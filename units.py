import unittest

from re import compile
class UnitError(Exception):
    __doc__="""Exception raised for unit conversion errors."""
class UnitConverter(object):
    PREFIXES={'G':1000000000.0,'M':1000000.0,'K':1000.0,'k':1000.0,'d':0.1,'c':0.01,'m':0.001,'n':0.000000001}
    UNITS={'m':{'SIVAL':1.0,'TYPE':'Length'},'ft':{'SIVAL':0.3048,'TYPE':'Length'},'s':{'SIVAL':1.0,'TYPE':'Time'},'min':{'SIVAL':60.0,'TYPE':'Time'},'kg':{'SIVAL':1.0,'TYPE':'Mass'},
           'g':{'SIVAL':0.001,'TYPE':'Mass'},'lb':{'SIVAL':2.2046226,'TYPE':'Mass'},'C':{'SIVAL':1.0,'TYPE':'Charge'},'hr':{'SIVAL':3600.0, 'TYPE':'Time'},'miles':{'SIVAL':1609.344,'TYPE':'Length'}}
    COMPOUND_UNITS={'A':{'SIVAL':1.0,'UNITS':'C/s'},'J':{'SIVAL':1.0,'UNITS':'kg*m**2/s**2'},'N':{'SIVAL':1.0,'UNITS':'kg*m/s**2'}}
    SEPARATORS={'MULTIPLY':'\*\*|\^|\*','DIVIDE':'\/'}
    def __init__(self,value=1,actualUnits=''):
        self.setunits(actualUnits)
        self.__setattr__('value',value)

        self.__setattr__('multiply',compile(self.SEPARATORS['MULTIPLY']))
        self.__setattr__('divide',compile(self.SEPARATORS['DIVIDE']))
    def setunits(self,actualUnits):
        self.__setattr__('actualUnits',actualUnits)
    def getUnit(self,unit):
        """getUnit(unit)
        Sub routine to extract unit parameters from UNITS dictionary and return the appropriate values.
        Also determines prefixes.
        """
        if unit in self.UNITS.keys():
            return self.UNITS[unit],1
        elif unit[1:] in self.UNITS.keys() and unit[0] in self.PREFIXES.keys():
            return self.UNITS[unit[1:]],self.PREFIXES[unit[0]]
        else:
            raise UnitError('Unit '+unit+' not found')
    def getCompoundUnit(self,order,scaling,unit):
        """getCompoundUnit(order,scaling,unit)
        Get compound unit parameters
        """
        if unit[1:] in self.COMPOUND_UNITS and unit[0] in self.PREFIXES.keys():
            scaling*=self.PREFIXES[unit[0]]
            unit=unit[1:]
        if unit not in self.COMPOUND_UNITS:
            raise UnitError('Unit '+unit+' not found')
        scaling*=self.COMPOUND_UNITS[unit]['SIVAL']
        units=dict(zip(['Numerator','Denominator'],[self.multiply.split('*'.join(self.divide.split(self.COMPOUND_UNITS[unit]['UNITS'])[::2])),self.multiply.split('*'.join(self.divide.split(self.COMPOUND_UNITS[unit]['UNITS'])[1::2]))]))
        newOrderNum,newScaling=self.unitParse(units['Numerator'])
        scaling*=newScaling
        newOrderDen,newScaling=self.unitParse(units['Denominator'])
        scaling/=newScaling
        for type in list(set(newOrderNum.keys()+newOrderDen.keys())):
            if not order.__contains__(type):
                order[type]=0
            try:
                order[type]+=newOrderNum[type]
            except KeyError:
                pass
            try:
                order[type]-=newOrderDen[type]
            except KeyError:
                pass
        return order,scaling
    def isCompound(self,unit):
        """isCompound(unit)
        Returns True if the unit is a compound unit (not a base SI unit)
        """
        if unit in self.COMPOUND_UNITS:
            return True
        elif unit[1:] in self.COMPOUND_UNITS and unit[0] in self.PREFIXES.keys():
            return True
        else:
            return False
    def unitParse(self,list):
        """unitParse(list)
        Parse a list of units and powers into a dimensional order and scaling factor to the SI UNIT combination.
        Expects list of the form [unit,(power),unit,..] where power doesn't have to be specified but if it does it refers to the previous unit.
        """
        #Give order of types and scaling to SI units
        scaling=1
        order={}
        for i in range(len(list)):
            unit=list[i]
            if unit=='':
                continue
            if unit.isdigit():
                if i==0:
                    raise UnitError('Cannot Parse unit incorrect format, number found before unit')
                else:
                    unit=list[i-1]
            if self.isCompound(unit):
                order,scaling=self.getCompoundUnit(order,scaling,unit)
                continue
            UnitParams=self.getUnit(unit)
            try:
                order[UnitParams[0]['TYPE']]+=1
            except KeyError:
                order[UnitParams[0]['TYPE']]=1
            scaling*=UnitParams[0]['SIVAL']*UnitParams[1]
        return order,scaling
    def combine(self,numerator,denominator):
        """combine(numeratorOrder,numeratorScaling,denominatorOrder,denominatorScaling)
        Combine numerator and denominator order and scaling into an overall order and scaling.
        """
        numeratorOrder=numerator[0]
        numeratorScaling=numerator[1]
        denominatorOrder=denominator[0]
        denominatorScaling=denominator[1]
        resultOrder={}
        for type in list(set(numeratorOrder.keys()+denominatorOrder.keys())):
            order=0
            try:
                order+=numeratorOrder[type]
            except KeyError:
                pass
            try:
                order-=denominatorOrder[type]
            except KeyError:
                pass
            resultOrder[type]=order
        scaling=numeratorScaling/denominatorScaling
        return resultOrder,scaling
    def compare(self,order1,order2):
        """compare(order1,order2)
        compare the dimensions of 2 sets of units and check that the result of dividing one by the other is dimensionless
        """
        for type in list(set(order1.keys()+order2.keys())):
            order=0
            try:
                order+=order1[type]
            except KeyError:
                pass
            try:
                order-=order2[type]
            except KeyError:
                pass
            if order!=0:
                return False
        return True
    def unitCompare(self,desiredUnit):
        """unitCompare(self,desiredUnit)
        Function to compare two units and return the scale factor between them.
        If the dimensional order of the units is incorrect raises an error.
        Expects forms:
        kg*m**2
        kg*m^2
        kg/m^3
        kg/m*m*m
        Splits for division first and then multiplication and power - no bracket parsing and assumes unit in the form:
        kg/m/s is kg per (m per s) ie kgs/m).
        """
        
        #Unit parsing into numerator and denominator
        actUnit=dict(zip(['Numerator','Denominator'],[self.multiply.split('*'.join(self.divide.split(self.actualUnits)[::2])),self.multiply.split('*'.join(self.divide.split(self.actualUnits)[1::2]))]))
        desUnit=dict(zip(['Numerator','Denominator'],[self.multiply.split('*'.join(self.divide.split(desiredUnit)[::2])),self.multiply.split('*'.join(self.divide.split(desiredUnit)[1::2]))]))
        #Determine values for the order and scaling of the units
        actUnitOrder,actUnitScaling=self.combine(self.unitParse(actUnit['Numerator']),self.unitParse(actUnit['Denominator']))
        desUnitOrder,desUnitScaling=self.combine(self.unitParse(desUnit['Numerator']),self.unitParse(desUnit['Denominator']))
        #If the orders match then return the scaling between them else raise an Error.
        #N.B. scaling is the number required to convert one of the unit type into the appropriate SI unit combination:
        #
        #   i.e. 100 ft/s= 30.48 m/s (SF=0.3048) && 1 km/s = 1000 m/s (SF=1000) so 1 ft/s is 0.03048 km/s
        # Therefore convert to meters and then to km so multiply by 0.3048 and divide by 1000
        if self.compare(actUnitOrder,desUnitOrder):
            return float(actUnitScaling)/float(desUnitScaling)
        else:
            raise UnitError('Order of units: '+self.actualUnits+'  and  '+desiredUnit+' does not match')
    def convert(self,desiredUnit):
        return self.unitCompare(desiredUnit)*self.value,desiredUnit
class __UnitConverterTestCase(unittest.TestCase):
    def setUp(self):
        self.__setattr__('unitConverter',UnitConverter())
    def tearDown(self):
        self.__delattr__('unitConverter')
    def test_setunits(self):
        self.unitConverter.setunits('kg/m**3')
        self.assertEqual(self.unitConverter.actualUnits,'kg/m**3')
    def test_getUnit(self):
        self.assertEqual(self.unitConverter.getUnit('m'),({'SIVAL':1.0,'TYPE':'Length'},1.0),'getUnit error: '+str(self.unitConverter.getUnit('m')))
        self.assertEqual(self.unitConverter.getUnit('km'),({'SIVAL':1.0,'TYPE':'Length'},1000.0),'getUnit error: '+str(self.unitConverter.getUnit('km')))
        self.assertEqual(self.unitConverter.getUnit('g'),({'SIVAL':0.001,'TYPE':'Mass'},1.0),'getUnit error: '+str(self.unitConverter.getUnit('g')))
        self.assertEqual(self.unitConverter.getUnit('kg'),({'SIVAL':1.0,'TYPE':'Mass'},1.0),'getUnit error: '+str(self.unitConverter.getUnit('kg')))
        self.assertEqual(self.unitConverter.getUnit('s'),({'SIVAL':1.0,'TYPE':'Time'},1.0),'getUnit error: '+str(self.unitConverter.getUnit('s')))
        self.assertEqual(self.unitConverter.getUnit('min'),({'SIVAL':60.0,'TYPE':'Time'},1.0),'getUnit error: '+str(self.unitConverter.getUnit('min')))
        self.assertEqual(self.unitConverter.getUnit('hr'),({'SIVAL':3600.0,'TYPE':'Time'},1.0),'getUnit error: '+str(self.unitConverter.getUnit('hr')))
        self.assertEqual(self.unitConverter.getUnit('miles'),({'SIVAL':1609.344,'TYPE':'Length'},1.0),'getUnit error: '+str(self.unitConverter.getUnit('miles')))
        self.assertEqual(self.unitConverter.getUnit('lb'),({'SIVAL':2.2046226,'TYPE':'Mass'},1.0),'getUnit error: '+str(self.unitConverter.getUnit('lb')))
        self.assertEqual(self.unitConverter.getUnit('Gs'),({'SIVAL':1.0,'TYPE':'Time'},1000000000.0),'getUnit error: '+str(self.unitConverter.getUnit('Gs')))
        self.assertEqual(self.unitConverter.getUnit('ft'),({'SIVAL':0.3048,'TYPE':'Length'},1.0),'getUnit error: '+str(self.unitConverter.getUnit('ft')))
        self.assertEqual(self.unitConverter.getUnit('MC'),({'SIVAL':1.0,'TYPE':'Charge'},1000000.0),'getUnit error: '+str(self.unitConverter.getUnit('MC')))
    def test_isCompound(self):
        self.assertTrue(self.unitConverter.isCompound('J'),'isCompound error: '+str(self.unitConverter.isCompound('J')))
        self.assertFalse(self.unitConverter.isCompound('m'),'isCompound error: '+str(self.unitConverter.isCompound('m')))
        self.assertTrue(self.unitConverter.isCompound('N'),'isCompound error: '+str(self.unitConverter.isCompound('N')))
        self.assertTrue(self.unitConverter.isCompound('A'),'isCompound error: '+str(self.unitConverter.isCompound('A')))
        self.assertFalse(self.unitConverter.isCompound('C'),'isCompound error: '+str(self.unitConverter.isCompound('C')))
        self.assertFalse(self.unitConverter.isCompound('g'),'isCompound error: '+str(self.unitConverter.isCompound('g')))
        self.assertFalse(self.unitConverter.isCompound('ft'),'isCompound error: '+str(self.unitConverter.isCompound('ft')))
        self.assertFalse(self.unitConverter.isCompound('lb'),'isCompound error: '+str(self.unitConverter.isCompound('lb')))
        self.assertFalse(self.unitConverter.isCompound('s'),'isCompound error: '+str(self.unitConverter.isCompound('s')))
        self.assertFalse(self.unitConverter.isCompound('min'),'isCompound error: '+str(self.unitConverter.isCompound('min')))
        self.assertFalse(self.unitConverter.isCompound('hr'),'isCompound error: '+str(self.unitConverter.isCompound('hr')))
        self.assertFalse(self.unitConverter.isCompound('miles'),'isCompound error: '+str(self.unitConverter.isCompound('miles')))
    def test_getCompoundUnit(self):
        self.assertEqual(self.unitConverter.getCompoundUnit({},1,'J'),({'Mass':1,'Length':2,'Time':-2},1),'getCompoundUnit error: '+str(self.unitConverter.getCompoundUnit({},1,'J')))
        self.assertEqual(self.unitConverter.getCompoundUnit({},1,'A'),({'Charge':1,'Time':-1},1),'getCompoundUnit error: '+str(self.unitConverter.getCompoundUnit({},1,'A')))
        self.assertEqual(self.unitConverter.getCompoundUnit({},1,'N'),({'Mass':1,'Length':1,'Time':-2},1),'getCompoundUnit error: '+str(self.unitConverter.getCompoundUnit({},1,'N')))
        self.assertEqual(self.unitConverter.getCompoundUnit({},1,'kN'),({'Mass':1,'Length':1,'Time':-2},1000.0),'getCompoundUnit error: '+str(self.unitConverter.getCompoundUnit({},1,'kN')))
    def test_unitParse(self):
        self.assertEqual(self.unitConverter.unitParse(['kJ','km']),({'Mass':1,'Length':3,'Time':-2},1000000),'unitParse error: '+str(self.unitConverter.unitParse(['kJ','km'])))
        self.assertEqual(self.unitConverter.unitParse(['kg','m']),({'Mass':1,'Length':1},1),'unitParse error: '+str(self.unitConverter.unitParse(['kg','m'])))
        self.assertEqual(self.unitConverter.unitParse(['Gs','ft']),({'Length':1,'Time':1},304800000.0),'unitParse error: '+str(self.unitConverter.unitParse(['Gs','ft'])))
    def test_combine(self):
        self.assertEqual(self.unitConverter.combine([{'Mass':1,'Length':4,'Time':-2},1000],[{'Mass':1,'Length':2},1000]),({'Mass':0,'Length':2,'Time':-2},1),'unitParse error: '+str(self.unitConverter.combine([{'Mass':1,'Length':4,'Time':-2},1000],[{'Mass':1,'Length':2},1000])))
        self.assertEqual(self.unitConverter.combine([{'Mass':3,'Length':4,'Time':-2},1000],[{'Mass':1,'Length':2},1000]),({'Mass':2,'Length':2,'Time':-2},1),'unitParse error: '+str(self.unitConverter.combine([{'Mass':3,'Length':4,'Time':-2},1000],[{'Mass':1,'Length':2},1000])))
    def test_compare(self):
        self.assertFalse(self.unitConverter.compare({'Mass':12,'Length':4,'Time':-2},{'Mass':1,'Length':4,'Time':-2}),'compare error: '+str(self.unitConverter.compare({'Mass':1,'Length':4,'Time':-2},{'Mass':1,'Length':4,'Time':-2})))
        self.assertFalse(self.unitConverter.compare({'Mass':12,'Length':4,'Time':-2},{'Mass':1,'Time':-2}),'compare error: '+str(self.unitConverter.compare({'Mass':1,'Length':4,'Time':-2},{'Mass':1,'Length':4,'Time':-2})))
        self.assertFalse(self.unitConverter.compare({'Mass':1,'Length':4,'Time':-2},{'Mass':1,'Length':14,'Time':-2}),'compare error: '+str(self.unitConverter.compare({'Mass':1,'Length':4,'Time':-2},{'Mass':1,'Length':4,'Time':-2})))
        self.assertFalse(self.unitConverter.compare({'Mass':1,'Length':4,'Time':2},{'Mass':1,'Length':4,'Time':-2}),'compare error: '+str(self.unitConverter.compare({'Mass':1,'Length':4,'Time':-2},{'Mass':1,'Length':4,'Time':-2})))
        self.assertTrue(self.unitConverter.compare({'Mass':1,'Length':4,'Time':-2},{'Mass':1,'Length':4,'Time':-2}),'compare error: '+str(self.unitConverter.compare({'Mass':1,'Length':4,'Time':-2},{'Mass':1,'Length':4,'Time':-2})))
    def test_unitCompare(self):
        self.unitConverter.setunits('m')
        self.assertAlmostEqual(self.unitConverter.unitCompare('ft'),3.28083989501,7,'unitCompare error: '+str(self.unitConverter.unitCompare('ft')))
        self.unitConverter.setunits('miles')
        self.assertEqual(self.unitConverter.unitCompare('m'),1609.344,'unitCompare error: '+str(self.unitConverter.unitCompare('m')))
        self.unitConverter.setunits('m')
        self.assertEqual(self.unitConverter.unitCompare('km'),0.001,'unitCompare error: '+str(self.unitConverter.unitCompare('km')))
    def test_convert(self):
        self.unitConverter.setunits('miles')
        self.unitConverter.value=123
        self.assertEqual(self.unitConverter.convert('m'),(1609.344*123,'m'),'unitCompare error: '+str(self.unitConverter.convert('m')))
def __debugTestSuite():
    suite=unittest.TestSuite()
    unitConverterSuite = unittest.TestLoader().loadTestsFromTestCase(__UnitConverterTestCase)
    suite.addTests(unitConverterSuite._tests)
    return suite
def __testSuite():
    unitConverterSuite = unittest.TestLoader().loadTestsFromTestCase(__UnitConverterTestCase)
    return unittest.TestSuite([unitConverterSuite])
def runTests():
    suite=__testSuite()
    unittest.TextTestRunner(verbosity=4).run(suite)
def debugTests():
    suite=__debugTestSuite()
    import ipdb,sys
    for test in suite:
        
        try:
            test.debug()
        except Exception,e:
            if type(e)==AssertionError:                
                ipdb.post_mortem(sys.exc_info()[2])
                
            else:
                try:
                    from IPython.core.ultratb import VerboseTB
                    vtb=VerboseTB(call_pdb=1)
                    vtb(*sys.exc_info())
                except:
                    import traceback
                    print'\n'
                    traceback.print_exc()
                ipdb.post_mortem(sys.exc_info()[2])
if  __name__=='__main__':
    runTests()