from cppad import *

def test_a_float_and_conditionals():
	x = a_float(2.)
	y = a_float(3.)
	z = a_float(2.)
	
	# assert that the conditionals work
	assert x == x
	assert x == z
	assert x != y
	assert x <= x
	assert x <= z
	assert x <= y
	assert x <  y
	
	# assert that conditionals can fail to be true
	assert not x == y
	assert not x != z
	assert not x != x
	assert not x >= y
	assert not x >  y
	
	
def test_a2float():
	x = a_float(2.)
	y = a_float(3.)
	z = a_float(2.)
	
	x = a2float(x)
	y = a2float(y)
	z = a2float(z)
	
	# assert that the conditionals work
	assert x == x
	assert x == z
	assert x != y
	assert x <= x
	assert x <= z
	assert x <= y
	assert x <  y
	
	# assert that conditionals can fail to be true
	assert not x == y
	assert not x != z
	assert not x != x
	assert not x >= y
	assert not x >  y	
	
def test_ad():
	x = ad(2.)
	y = ad(3.)
	z = ad(2.)
	
	# assert that the conditionals work
	assert x == x
	assert x == z
	assert x != y
	assert x <= x
	assert x <= z
	assert x <= y
	assert x <  y
	
	# assert that conditionals can fail to be true
	assert not x == y
	assert not x != z
	assert not x != x
	assert not x >= y
	assert not x >  y		
	
	x = ad(x)
	y = ad(y)
	z = ad(z)
	
	# assert that the conditionals work
	assert x == x
	assert x == z
	assert x != y
	assert x <= x
	assert x <= z
	assert x <= y
	assert x <  y
	
	# assert that conditionals can fail to be true
	assert not x == y
	assert not x != z
	assert not x != x
	assert not x >= y
	assert not x >  y
	
def test_array_element_type_is_int():
	x = array( [ 1 ] )
	a_x = independent(x)
	a_y = a_x
	f = adfun(a_x, a_y) 
	y = f.forward(0, x) 
	assert y[0] == 1
	
def test_elementary_a_float_operations():
	x = a_float(2.)
	y = a_float(3.)
	
	assert x + y == a_float(5.)
	assert x - y == a_float(-1.)
	assert x * y == a_float(6.)
	assert x / y == a_float(2./3.)
	
	x += y
	assert x == ad(5.)
	x -= y
	assert x == ad(2.)
	
def test_elementary_ad_operations():
	x = ad(2.)
	y = ad(3.)
	
	assert x + y == ad(5.)
	assert x - y == ad(-1.)
	assert x * y == ad(6.)
	assert x / y == ad(2./3.)
	
	x += y
	assert x == ad(5.)
	x -= y
	assert x == ad(2.)	
		
def test_a_float_variable_info():
	x = ad(2.)
	y = ad(x)
	print x
	print y
	print x
	
	assert x.__str__() == '2'
	assert value(x)     == 2.
	# assert x.id        == 1
	# assert x.taddr     == 0
	
def test_ad_a_float_variable_info():
	x = ad(ad(13.0))
	print x
	
	assert x.__str__() ==  '13'
	assert value(value(x)) == 13.
	# assert x.id == 1
	# assert x.taddr == 0	
	
def test_trigonometic_functions():
	N = 5
	x  = array( [ 2.*n*numpy.pi/N     for n in range(N) ] )
	
	# cos
	ax = independent(x)
	ay = numpy.cos(ax)
	af = adfun(ax, ay)
	J = af.jacobian(x)
	
	assert numpy.sum( abs( numpy.diag( numpy.sin(x)) + J)) == 0
	
	# sin
	ax = independent(x)
	ay = numpy.sin(ax)
	af = adfun(ax, ay)
	J = af.jacobian(x)
	assert numpy.prod( numpy.diag( numpy.cos(x)) == J)


def test_pow():
	x   = array( [ 3, 2] )
	ax  = array( [ ad(x[0]), ad(x[1])] )
	ay = array([ ax[0]**2, ax[1]**2, ax[0]**2., ax[1]**2., ax[0]**0.5, ax[1]**0.5, ax[0]**ad(2), ax[1]**ad(2)])
	y = array([ x[0]**2, x[1]**2, x[0]**2., x[1]**2., x[0]**0.5, x[1]**0.5, x[0]**2, x[1]**2])
	
	assert numpy.prod(ay == y)
	

def test_multi_level_taping_and_higher_order_forward_derivatives():
	ok = True
	level = 1
	x = array( [ 2 , 3 ] )
	ad_x = independent(x)
	# declare level two independent variable vector and start level two recording
	level = 2
	ad_ad_x = independent(ad_x)
	# declare level 2 dependent variable vector and stop level 2 recording
	ad_ad_y = array( [ 2. * ad_ad_x[0] * ad_ad_x[1] ] )
	ad_f = adfun(ad_ad_x, ad_ad_y) # f(x0, x1) = 2. * x0 * x1
	# evaluate the function f(x) using level one independent variable vector
	p  = 0
	ad_fp = ad_f.forward(p, ad_x)
	ok = ok and (ad_fp == 2. * ad_x[0] * ad_x[1])
	# evaluate the partial of f with respect to the first component
	p  = 1
	ad_xp = array( [ ad(1.) , ad(0.) ] )
	ad_fp = ad_f.forward(p, ad_xp)
	ok = ok and (ad_fp == 2. * ad_x[1])
	# declare level 1 dependent variable vector and stop level 1 recording 
	ad_y = 2. * ad_fp
	g = adfun(ad_x, ad_y) # g(x0, x1) = 2. * partial_x0 f(x0, x1) = 4 * x1
	# evaluate the function g(x) at x = (4,5)
	p  = 0
	x  = array( [ 4. , 5. ] )
	gp = g.forward(p, x)
	ok = ok and (gp == 4. * x[1])
	# evaluate the partial of g with respect to x0
	p  = 1
	xp = array( [ 1. , 0. ] )
	gp = g.forward(p, xp)
	ok = ok and (gp == 0.)
	# evaluate the partial of g with respect to x1
	p  = 1
	xp = array( [ 0. , 1. ] )
	gp = g.forward(p, xp)
	ok = ok and (gp == 4.)
	
	assert ok

def test_multi_level_taping_and_higher_order_reverse_derivatives():

	# domain space vector
	x = array([0., 1.])

	# declare independent variables and start recording
	ax = independent(x);

	ay = array([ax[0] * ax[0] * ax[1]])

	# create f : X -> Y and stop recording
	af = adfun (ax, ay);

	# use first order reverse mode to evaluate derivative of y[0]
	# and use the values in X for the independent variables.
	w = numpy.zeros(1)
	w[0] = 1.

	y = af.forward(0, array([0.,1.]))
	dw = af.reverse(1, w);
	assert dw[0] == 2.*ax[0]*ax[1]
	assert dw[1] == ax[0]*ax[0]

	# use zero order forward mode to evaluate y at x = (3, 4)
	# and use the template parameter Vector for the vector type

	x =  array([3.,4.])
	y = af.forward(0,x)
	assert y[0] == x[0]*x[0]*x[1]

	# use first order reverse mode to evaluate derivative of y[0]
	# and using the values in x for the independent variables.
	w[0] = 1.
	dw   = af.reverse(1, w)
	
	assert dw[0] ==  2.*x[0]*x[1]
	assert dw[1] ==   x[0]*x[0]
	
def test_jacobian():
	N = 4
	A = array([n+1. for n in range(N*N)]).reshape((N,N))
	def f(x):
		return numpy.dot(A,x)
	
	x = array([0. for n in range(N) ])
	ax = independent(x)
	ay = f(ax)
	af = adfun (ax, ay);
	x = array([1. for n in range(N)])
	
	J = af.jacobian(x)
	
	assert numpy.prod( A == J )
	
#def test_hessian():
#	N = 4
#	A = numpy.ones((N,N)) + 2.*numpy.eye(N)
#	def f(x):
#		return array([0.5* numpy.dot(x,numpy.dot(A,x))])
#	
#	x = array([0. for n in range(N) ])
#	ax = independent(x)
#	ay = f(ax)
#	af = adfun (ax, ay);
#	x = array([1. for n in range(N)])
#	H = af.hessian(x)
#
#	assert numpy.prod( A == H )
#

