import unittest
from re import compile
class UnitError(Exception):
    __doc__="""Exception raised for unit conversion errors."""
class Unit(float):
    _prefixes={'G':1000000000.0,'M':1000000.0,'K':1000.0,'k':1000.0,'d':0.1,'c':0.01,'m':0.001,'n':0.000000001}
    _units={'m':{'SIVAL':1.0,'TYPE':'Length'},'ft':{'SIVAL':0.3048,'TYPE':'Length'},'s':{'SIVAL':1.0,'TYPE':'Time'},'min':{'SIVAL':60.0,'TYPE':'Time'},'kg':{'SIVAL':1.0,'TYPE':'Mass'},
           'g':{'SIVAL':0.001,'TYPE':'Mass'},'lb':{'SIVAL':2.2046226,'TYPE':'Mass'},'C':{'SIVAL':1.0,'TYPE':'Charge'},'hr':{'SIVAL':3600.0, 'TYPE':'Time'},'miles':{'SIVAL':1609.344,'TYPE':'Length'}}
    _compoundUnits={'Ohm':{'SIVAL':1.0,'UNITS':'kg*m**2/s*C**2'},'A':{'SIVAL':1.0,'UNITS':'C/s'},'J':{'SIVAL':1.0,'UNITS':'kg*m**2/s**2'},'N':{'SIVAL':1.0,'UNITS':'kg*m/s**2'},'V':{'SIVAL':1.0,'UNITS':'kg*m**2/C*s**2'}}
    _separators={'MULTIPLY':'\*\*|\^|\*','DIVIDE':'\/'}
    def __init__(self,value,units=False):
        super(Unit,self).__init__(value)
        if units:
            self.setUnits(units)
        else:
            self.__setattr__('units',False)
            self.__setattr__('order',False)
    def setUnits(self,units):
        multiply=compile(self._separators['MULTIPLY'])
        divide=compile(self._separators['DIVIDE'])
        actUnit=dict(zip(['Numerator','Denominator'],[multiply.split('*'.join(divide.split(units)[::2])),multiply.split('*'.join(divide.split(units)[1::2]))]))
        #Determine values for the order and scaling of the units
        order,scaling=self.combine(self.unitParse(actUnit['Numerator']),self.unitParse(actUnit['Denominator']))
        self.__setattr__('units',units)
        self.__setattr__('order',order)
    def __eq__(self,other):
        if type(other)==type(self):
            #check order and then convert to unit
            if not other.order or other.order==self.order:
                return super(Unit,self).__eq__(other.convert(self.units))
            return False
        else:
            return super(Unit,self).__eq__(other)
    def __ne__(self,other):
        return not self==other
    def __add__(self,other):
        if type(other)==type(self):
            #check order and then convert to unit
            if not other.order or other.order==self.order:
                return super(Unit,self).__add__(other.convert(self.units))
            raise UnitError('Dimensionality of units does not match')
        else:
            return super(Unit,self).__add__(other)
    def __sub__(self,other):
        if type(other)==type(self):
            #check order and then convert to unit
            if not other.order or other.order==self.order:
                return super(Unit,self).__sub__(other.convert(self.units))
            raise UnitError('Dimensionality of units does not match')
        else:
            return super(Unit,self).__sub__(other)
    def __mul__(self,other):
        if type(other)==type(self):
            #check order and then convert to unit
            if not other.order or other.order==self.order:
                return super(Unit,self).__mul__(other.convert(self.units))
            elif not other.order:
                newValue=float(self)*float(other)
                return self.__new__(newValue,self.units.split('/')[0]+'*'+other.units.split('/')[0]+'/'+self.units.split('/')[1]+'*'+other.units.split('/')[1])
            raise UnitError('Dimensionality of units does not match')
        else:
            return super(Unit,self).__mul__(other)
    def __div__(self,other):
        if type(other)==type(self):
            #check order and then convert to unit
            if not other.order or other.order==self.order:
                return super(Unit,self).__div__(other.convert(self.units))
            elif not other.order:
                newValue=float(self)*float(other)
                return self.__new__(newValue,self.units.split('/')[0]+'*'+other.units.split('/')[1]+'/'+self.units.split('/')[1]+'*'+other.units.split('/')[0])
            raise UnitError('Dimensionality of units does not match')
        else:
            return super(Unit,self).__div__(other)
    def __truediv__(self,other):
        if type(other)==type(self):
            #check order and then convert to unit
            if not other.order or other.order==self.order:
                return super(Unit,self).__truediv__(other.convert(self.units))
            elif not other.order:
                newValue=float(self)*float(other)
                return self.__new__(newValue,self.units.split('/')[0]+'*'+other.units.split('/')[1]+'/'+self.units.split('/')[1]+'*'+other.units.split('/')[0])
            raise UnitError('Dimensionality of units does not match')
        else:
            return super(Unit,self).__truediv__(other)
    def __mod__(self,other):
        if type(other)==type(self):
            #check order and then convert to unit
            if not other.order or other.order==self.order:
                return super(Unit,self).__mod__(other.convert(self.units))
            raise UnitError('Dimensionality of units does not match')
        else:
            return super(Unit,self).__mod__(other)
    def __pow__(self,other):
        if type(other)==type(self):
            #check order and then convert to unit
            if not other.order:
                return super(Unit,self).__pow__(other.convert(self.units))
            raise UnitError('Cannot raise to the power of a value with units')
        else:
            return super(Unit,self).__pow__(other)
    def __divmod__(self,other):
        if type(other)==type(self):
            #check order and then convert to unit
            if not other.order or other.order==self.order:
                return super(Unit,self).__divmod__(other.convert(self.units))
            raise UnitError('Dimensionality of units does not match')
        else:
            return super(Unit,self).__divmod__(other)
    def __ge__(self,other):
        if type(other)==type(self):
            #check order and then convert to unit
            if not other.order or other.order==self.order:
                return super(Unit,self).__ge__(other.convert(self.units))
            raise UnitError('Dimensionality of units does not match')
        else:
            return super(Unit,self).__ge__(other)
    def __gt__(self,other):
        if type(other)==type(self):
            #check order and then convert to unit
            if not other.order or other.order==self.order:
                return super(Unit,self).__gt__(other.convert(self.units))
            raise UnitError('Dimensionality of units does not match')
        else:
            return super(Unit,self).__gt__(other)
    def __le__(self,other):
        if type(other)==type(self):
            #check order and then convert to unit
            if not other.order or other.order==self.order:
                return super(Unit,self).__le__(other.convert(self.units))
            raise UnitError('Dimensionality of units does not match')
        else:
            return super(Unit,self).__le__(other)
    def __lt__(self,other):
        if type(other)==type(self):
            #check order and then convert to unit
            if not other.order or other.order==self.order:
                return super(Unit,self).__lt__(other.convert(self.units))
            raise UnitError('Dimensionality of units does not match')
        else:
            return super(Unit,self).__lt__(other)
    def getUnit(self,unit):
        """getUnit(unit)
        Sub routine to extract unit parameters from UNITS dictionary and return the appropriate values.
        Also determines prefixes.
        """
        if unit in self._units.keys():
            return self._units[unit],1
        elif unit[1:] in self._units.keys() and unit[0] in self._prefixes.keys():
            return self._units[unit[1:]],self._prefixes[unit[0]]
        else:
            raise UnitError('Unit '+unit+' not found')
    def getCompoundUnit(self,order,scaling,unit):
        """getCompoundUnit(order,scaling,unit)
        Get compound unit parameters
        """
        multiply=compile(self._separators['MULTIPLY'])
        divide=compile(self._separators['DIVIDE'])
        if unit[1:] in self._compoundUnits and unit[0] in self._prefixes.keys():
            scaling*=self._prefixes[unit[0]]
            unit=unit[1:]
        if unit not in self._compoundUnits:
            raise UnitError('Unit '+unit+' not found')
        scaling*=self._compoundUnits[unit]['SIVAL']
        units=dict(zip(['Numerator','Denominator'],[multiply.split('*'.join(divide.split(self._compoundUnits[unit]['UNITS'])[::2])),multiply.split('*'.join(divide.split(self._compoundUnits[unit]['UNITS'])[1::2]))]))
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
        if unit in self._compoundUnits:
            return True
        elif unit[1:] in self._compoundUnits and unit[0] in self._prefixes.keys():
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

        multiply=compile(self._separators['MULTIPLY'])
        divide=compile(self._separators['DIVIDE'])
        
        #Unit parsing into numerator and denominator
        actUnit=dict(zip(['Numerator','Denominator'],[multiply.split('*'.join(divide.split(self.units)[::2])),multiply.split('*'.join(divide.split(self.units)[1::2]))]))
        desUnit=dict(zip(['Numerator','Denominator'],[multiply.split('*'.join(divide.split(desiredUnit)[::2])),multiply.split('*'.join(divide.split(desiredUnit)[1::2]))]))
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
            raise UnitError('Order of units: '+self.units+'  and  '+desiredUnit+' does not match')
    def convert(self,unit):
        return self*self.unitCompare(unit)
class __UnitTestCase(unittest.TestCase):
    def setUp(self):
        self.__setattr__('unit',Unit(1))
    def tearDown(self):
        self.__delattr__('unit')
    def test_setunits(self):
        self.unit.setUnits('kg/m**3')
        self.assertEqual(self.unit.units,'kg/m**3')
    def test_getUnit(self):
        self.assertEqual(self.unit.getUnit('m'),({'SIVAL':1.0,'TYPE':'Length'},1.0),'getUnit error: '+str(self.unit.getUnit('m')))
        self.assertEqual(self.unit.getUnit('km'),({'SIVAL':1.0,'TYPE':'Length'},1000.0),'getUnit error: '+str(self.unit.getUnit('km')))
        self.assertEqual(self.unit.getUnit('g'),({'SIVAL':0.001,'TYPE':'Mass'},1.0),'getUnit error: '+str(self.unit.getUnit('g')))
        self.assertEqual(self.unit.getUnit('kg'),({'SIVAL':1.0,'TYPE':'Mass'},1.0),'getUnit error: '+str(self.unit.getUnit('kg')))
        self.assertEqual(self.unit.getUnit('s'),({'SIVAL':1.0,'TYPE':'Time'},1.0),'getUnit error: '+str(self.unit.getUnit('s')))
        self.assertEqual(self.unit.getUnit('min'),({'SIVAL':60.0,'TYPE':'Time'},1.0),'getUnit error: '+str(self.unit.getUnit('min')))
        self.assertEqual(self.unit.getUnit('hr'),({'SIVAL':3600.0,'TYPE':'Time'},1.0),'getUnit error: '+str(self.unit.getUnit('hr')))
        self.assertEqual(self.unit.getUnit('miles'),({'SIVAL':1609.344,'TYPE':'Length'},1.0),'getUnit error: '+str(self.unit.getUnit('miles')))
        self.assertEqual(self.unit.getUnit('lb'),({'SIVAL':2.2046226,'TYPE':'Mass'},1.0),'getUnit error: '+str(self.unit.getUnit('lb')))
        self.assertEqual(self.unit.getUnit('Gs'),({'SIVAL':1.0,'TYPE':'Time'},1000000000.0),'getUnit error: '+str(self.unit.getUnit('Gs')))
        self.assertEqual(self.unit.getUnit('ft'),({'SIVAL':0.3048,'TYPE':'Length'},1.0),'getUnit error: '+str(self.unit.getUnit('ft')))
        self.assertEqual(self.unit.getUnit('MC'),({'SIVAL':1.0,'TYPE':'Charge'},1000000.0),'getUnit error: '+str(self.unit.getUnit('MC')))
    def test_isCompound(self):
        self.assertTrue(self.unit.isCompound('J'),'isCompound error: '+str(self.unit.isCompound('J')))
        self.assertFalse(self.unit.isCompound('m'),'isCompound error: '+str(self.unit.isCompound('m')))
        self.assertTrue(self.unit.isCompound('N'),'isCompound error: '+str(self.unit.isCompound('N')))
        self.assertTrue(self.unit.isCompound('A'),'isCompound error: '+str(self.unit.isCompound('A')))
        self.assertTrue(self.unit.isCompound('A'),'isCompound error: '+str(self.unit.isCompound('A')))
        self.assertTrue(self.unit.isCompound('V'),'isCompound error: '+str(self.unit.isCompound('V')))
        self.assertTrue(self.unit.isCompound('Ohm'),'isCompound error: '+str(self.unit.isCompound('Ohm')))
        self.assertFalse(self.unit.isCompound('C'),'isCompound error: '+str(self.unit.isCompound('C')))
        self.assertFalse(self.unit.isCompound('g'),'isCompound error: '+str(self.unit.isCompound('g')))
        self.assertFalse(self.unit.isCompound('ft'),'isCompound error: '+str(self.unit.isCompound('ft')))
        self.assertFalse(self.unit.isCompound('lb'),'isCompound error: '+str(self.unit.isCompound('lb')))
        self.assertFalse(self.unit.isCompound('s'),'isCompound error: '+str(self.unit.isCompound('s')))
        self.assertFalse(self.unit.isCompound('min'),'isCompound error: '+str(self.unit.isCompound('min')))
        self.assertFalse(self.unit.isCompound('hr'),'isCompound error: '+str(self.unit.isCompound('hr')))
        self.assertFalse(self.unit.isCompound('miles'),'isCompound error: '+str(self.unit.isCompound('miles')))
    def test_getCompoundUnit(self):
        self.assertEqual(self.unit.getCompoundUnit({},1,'J'),({'Mass':1,'Length':2,'Time':-2},1),'getCompoundUnit error: '+str(self.unit.getCompoundUnit({},1,'J')))
        self.assertEqual(self.unit.getCompoundUnit({},1,'A'),({'Charge':1,'Time':-1},1),'getCompoundUnit error: '+str(self.unit.getCompoundUnit({},1,'A')))
        self.assertEqual(self.unit.getCompoundUnit({},1,'V'),({'Length': 2, 'Mass': 1, 'Charge': -1, 'Time': -2},1),'getCompoundUnit error: '+str(self.unit.getCompoundUnit({},1,'V')))
        self.assertEqual(self.unit.getCompoundUnit({},1,'Ohm'),({'Length': 2, 'Mass': 1, 'Charge': -2, 'Time': -1},1),'getCompoundUnit error: '+str(self.unit.getCompoundUnit({},1,'Ohm')))
        self.assertEqual(self.unit.getCompoundUnit({},1,'N'),({'Mass':1,'Length':1,'Time':-2},1),'getCompoundUnit error: '+str(self.unit.getCompoundUnit({},1,'N')))
        self.assertEqual(self.unit.getCompoundUnit({},1,'kN'),({'Mass':1,'Length':1,'Time':-2},1000.0),'getCompoundUnit error: '+str(self.unit.getCompoundUnit({},1,'kN')))
    def test_unitParse(self):
        self.assertEqual(self.unit.unitParse(['kJ','km']),({'Mass':1,'Length':3,'Time':-2},1000000),'unitParse error: '+str(self.unit.unitParse(['kJ','km'])))
        self.assertEqual(self.unit.unitParse(['kg','m']),({'Mass':1,'Length':1},1),'unitParse error: '+str(self.unit.unitParse(['kg','m'])))
        self.assertEqual(self.unit.unitParse(['Gs','ft']),({'Length':1,'Time':1},304800000.0),'unitParse error: '+str(self.unit.unitParse(['Gs','ft'])))
    def test_combine(self):
        self.assertEqual(self.unit.combine([{'Mass':1,'Length':4,'Time':-2},1000],[{'Mass':1,'Length':2},1000]),({'Mass':0,'Length':2,'Time':-2},1),'unitParse error: '+str(self.unit.combine([{'Mass':1,'Length':4,'Time':-2},1000],[{'Mass':1,'Length':2},1000])))
        self.assertEqual(self.unit.combine([{'Mass':3,'Length':4,'Time':-2},1000],[{'Mass':1,'Length':2},1000]),({'Mass':2,'Length':2,'Time':-2},1),'unitParse error: '+str(self.unit.combine([{'Mass':3,'Length':4,'Time':-2},1000],[{'Mass':1,'Length':2},1000])))
    def test_compare(self):
        self.assertFalse(self.unit.compare({'Mass':12,'Length':4,'Time':-2},{'Mass':1,'Length':4,'Time':-2}),'compare error: '+str(self.unit.compare({'Mass':1,'Length':4,'Time':-2},{'Mass':1,'Length':4,'Time':-2})))
        self.assertFalse(self.unit.compare({'Mass':12,'Length':4,'Time':-2},{'Mass':1,'Time':-2}),'compare error: '+str(self.unit.compare({'Mass':1,'Length':4,'Time':-2},{'Mass':1,'Length':4,'Time':-2})))
        self.assertFalse(self.unit.compare({'Mass':1,'Length':4,'Time':-2},{'Mass':1,'Length':14,'Time':-2}),'compare error: '+str(self.unit.compare({'Mass':1,'Length':4,'Time':-2},{'Mass':1,'Length':4,'Time':-2})))
        self.assertFalse(self.unit.compare({'Mass':1,'Length':4,'Time':2},{'Mass':1,'Length':4,'Time':-2}),'compare error: '+str(self.unit.compare({'Mass':1,'Length':4,'Time':-2},{'Mass':1,'Length':4,'Time':-2})))
        self.assertTrue(self.unit.compare({'Mass':1,'Length':4,'Time':-2},{'Mass':1,'Length':4,'Time':-2}),'compare error: '+str(self.unit.compare({'Mass':1,'Length':4,'Time':-2},{'Mass':1,'Length':4,'Time':-2})))
    def test_unitCompare(self):
        self.unit.setUnits('m')
        self.assertAlmostEqual(self.unit.unitCompare('ft'),3.28083989501,7,'unitCompare error: '+str(self.unit.unitCompare('ft')))
        self.unit.setUnits('miles')
        self.assertEqual(self.unit.unitCompare('m'),1609.344,'unitCompare error: '+str(self.unit.unitCompare('m')))
        self.unit.setUnits('m')
        self.assertEqual(self.unit.unitCompare('km'),0.001,'unitCompare error: '+str(self.unit.unitCompare('km')))
    def test_convert(self):
        self.unit=Unit(123)
        self.unit.setUnits('miles')
        self.assertEqual(self.unit.convert('m'),1609.344*123,'unitCompare error: '+str(self.unit.convert('m')))
def __debugTestSuite():
    suite=unittest.TestSuite()
    unitSuite = unittest.TestLoader().loadTestsFromTestCase(__UnitTestCase)
    suite.addTests(unitSuite._tests)
    return suite
def __testSuite():
    unitSuite = unittest.TestLoader().loadTestsFromTestCase(__UnitTestCase)
    return unittest.TestSuite([unitSuite])
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