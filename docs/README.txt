plonesocial.auth.rpx
====================

`plonesocial.auth.rpx` is an addon product for Plone which allows users
to authenticate via the `JanRain's RPX service <http://rpxnow.com>`_. RPX is
sort of a proxy to let a user authenticate with a lot of identity services such
as OpenID, Twitter, Facebook and many others.

Different from the OpenID plugin for Plone the RPX plugin does not just create a virtual user but instead it will map the verfied identifier from RPX (e.g. your OpenID) to an existing or to be created user account. A user is also able to map various identifiers to the same Plone account thus being able to login with his Twitter, Google or Facebook account to the same Plone account. 

`plonesocial.auth.rpx` also allows the user to manage those mappings.

Documentation
=============

The full documentation can be found at http://comlounge.net/rpx/

Please report bug at http://bitbucket.org/cryu/plonesocial.auth.rpx/issues/

Credits
=======

* Carsten Rebbien (main programming, cr@comlounge.net)
* Christian Scholz (concept, bugfixing and documentation, cs@comlounge.net)

Source Code
===========

The source code is available at http://bitbucket.org/cryu/plonesocial.auth.rpx/

License
=======

Copyright (c) 2010 COM.lounge GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


