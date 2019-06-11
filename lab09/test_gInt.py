import sys
import unittest

from gInt import gInt 

class gIntTest( unittest.TestCase ) :
        '''Tests for gInt class'''

        def setUp( self ) :
                '''Optional.  Run before for each test.'''
                self.u1 = gInt( 1, 2 )
                self.u1copy = gInt( 1, 2 )
                self.u2 = gInt(  3, 4 )
                self.u2copy = gInt(  3, 4 )
                self.p1 = gInt( 13, 13 )
                self.n1 = gInt( -13, -13 )
                self.n2 = gInt( -13, 13 )
                self.n3 = gInt( 13, -13)
                self.n3copy = gInt( 13, -13 )

        def tearDown( self ) :
                '''Optional.  Called after each test (if setUp didn't fail)'''
                pass

        def test_norm( self ) :
                norm = self.u1.norm()

                self.assertEqual( self.u1, self.u1, 'gInt not equal to itself' )
                self.assertEqual( self.u1, self.u1copy, 'gInt not equal to identical object' )
                self.assertEqual( self.u1.norm(), norm, 'Invoked method returns differnt result than stored value' )
                self.assertEqual( norm, 1**2 + 2**2, 'Result of norm not eqaul to literal value')

                self.assertNotEqual( self.u1.norm(), self.u2.norm(), 'norm of gInt(1,2) == norm of gInt(3,4)' )
                self.assertEqual( self.n1.norm(), self.n2.norm(), 'gInt(-13,-13) != gInt(-13,13)' )
                self.assertEqual( self.n2.norm(), self.n3.norm(), 'gInt(-13,13) != gInt(13,-13)' )

        def test_add( self ) :

                sum1 = self.u1 + self.u2
                self.assertEqual( self.u1, self.u1copy, 'Left operand changed after addition' )
                self.assertEqual( self.u2, self.u2copy, 'Right operand changed after addition' )
                self.assertEqual( self.u1 + self.u2, gInt( 4, 6 ), 'Addition failed' )

                sum2 = self.u1 + self.n1
                self.assertEqual(sum2, gInt( -12, -11 ), 'Addition of positive + negative failed' )

                sum3 = self.n1 + self.n2
                self.assertEqual( sum3, gInt( -26, 0 ), 'Addition of negative + negative failed' )
        
        def test_mul( self ) :

                prod1 = self.u1 * self.u2
                self.assertEqual( self.u1, self.u1copy, 'Left operand changed after multiplication' )
                self.assertEqual( self.u2, self.u2copy, 'Right operand changed after multiplication' )
                self.assertEqual( prod1, gInt( -5, 10 ), 'Multiplication failed' )

                prod2 = self.u1 * self.n1
                self.assertEqual(prod2, gInt( 13, -39 ), 'Multiplication of positive + negative failed' )

                prod3 = self.n1 * self.n2
                self.assertEqual( prod3, gInt( 338, 0 ), 'Multiplication of negative + negative failed' )

if __name__ == '__main__' :
        unittest.main()
