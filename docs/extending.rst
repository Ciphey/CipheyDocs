Extending Ciphey
================

The biggest change in Orwell is the revamped interface. It is now very simple to add your own
cipher, checker, decoding or even search algorithm!

All of these interfaces (and more) can be found in the ``ciphey/iface`` directory,
which you should definitely refer to as you go!

Ciphey uses camelCase for abstract method names, so it is more easy to spot them
in your (and our!) code.


.. contents::


Registering your module
-----------------------

Ciphey has a singleton Registry object that keeps track of all of the modules.
After getting your code imported with ``-m`` (or by integrating it into the source),
your class must use one of the following decorators:

``@ciphey.iface.registry.register`` examines the decorated class to determine what
interface it uses, and then registers it:

.. code:: python

  from ciphey.iface import registry, Cracker

  @registry.register
  class DesBruteForce(Cracker[bytes]):
      pass

This covers pretty much every use case, but there may exist a case where the class
can accept multiple different types, such as for some ``ResourceLoaders``. In this
case, you should use ``@ciphey.iface.registry.register_multi``:

.. code:: python

  from ciphey.iface import registry, Decoder

  @registry.register_multi((str, str), (bytes, bytes))
  class Reverse(Decoder):
      pass

  @registry.register_multi(str, bytes)
  class EveryNthSymbol(Cracker):
      pass

Note how the type parameters are not given to the interface name; these are filled in
by the decorator

Base classes
------------
These provide various attributes of the module you wish to add:

ConfigurableModule
^^^^^^^^^^^^^^^^^^
The ``ConfigurableModule`` interface forms the basis of all modules, and has
two abstract methods (methods that *must* be implemented in any derived class)

First, you must have an ``__init__(self, config: Config)`` method, which is how
your object will be constructed. You must also invoke the base class's
constructor with ``super().__init__(config)`` inside your override.

Secondly, you must implement ``getParams() -> Optional[Dict[str, ParamSpec]]``.
This method should return ``None`` if there are no parameters, and a dictionary
with elements ``param_name: param_spec``. This parameter specification object
has a large range of fields, which can be found in the source code.

Targeted
^^^^^^^^
The ``Targeted`` interface only has one abstract static method:
``getTarget() -> str``. This should return the name of the cipher/encoding this
module attacks, so that users can gather all of the modules for a specific
target.

Checker
-------
The checker is a simple interface used to determine whether a given result is
the sought-after plaintext. There exists a simple ``regex`` checker, and a
``brandon`` natural language checker, but it is perfectly possible that these
do not fulfill your needs. It has two abstract methods:

``check(self, text: T) -> Optional[str]`` should check to see if ``text`` is
the solution. It should then return a ``str containing information about how it
worked out it was the solution (or an empty string if this isn't possible),
or ``None`` if it wasn't the solution.

``getExpectedRuntime() -> float`` should be used to give a rough idea about how
many seconds this should take to run. If you don't know, a value of ``1`` is
absolutely fine.

Cracker
-------
This interface is what you likely came here for, it represents a system for
cracking ciphers. This has 2 abstract methods:

``getInfo(self, ctext: T) -> CrackInfo`` is a more refined form of the
``priority`` method of ``Decoder``. It should make an accurate assessment of
how likely it is that it will crack the code (including the likelihood that this
is even the cipher that has been used), as well as the time taken if it succeeds
or fails. Do not spend too long calculating this, but a greater accuracy will
allow the ``Searcher`` to be more efficient.

``attemptCrack(self, ctext: T) -> List[CrackResult]`` actually performs the
cracking. It should return an empty list on failure, or a list of potential
ciphertexts (please not too many!), with keys and other information if it is
appropriate. The CrackResult class is also located in ``iface.py``, and is
pretty self-explanatory.

Decoder
-------
The decoder represents the undoing of some encoding, and is the only module
capable of translating between data types. As such, it has two type parameters.
The first (``T``) is the source type, and the last (``U``) is the destination
type. It has two abstract methods:

``decode(self, ctext: T) -> Optional[U]`` does pretty much what you expect. It
attempts to decode some data ``ctext``, returning ``None`` on failure. Be aware
that most of the data passed to this function will not be of your decoding, so
it is worth optimising towards recognising false candidates rather than towards
decoding correctly passed data.

``priority() -> float`` is an static method that should return a very rough
estimate of the liklihood that this encoding will turn up.
``Base64`` and ``Base16`` have this set to ``0.4``,
whereas ``Morse`` has this set to ``0.05``. Use that as a rough guide.

ResourceLoader
--------------
This is a rather odd interface, and sits rather awkwardly with the rest of
Ciphey. Resource loaders are responsible for loading distributions and wordlists
(and potentially other data) from some source, be it from the filesystem, the
Internet, or even dynamically generated. Before adding your own, check if the
``Json``, ``Csv`` or ``CipheyDists`` resource loaders fit your needs already.

The first abstract method is ``whatResources(self)``, which should return
a list of the names of resources that can be provided by this module, or
``None`` if this list cannot easily be obtained.

The esecond is ``getResource(self, name: str) -> T``, which should return the
named resource. Bear in mind that this function may be called with something
that was not returned from ``whatResources``, and should handle it with some
form of exception where appropriate.

Searcher
--------
This is the heart of Ciphey, and is what sets it above similar tools. It must
intelligently work out how to crack the ciphertext using the modules found
in the registry. It took us more than a month to come to ``AuSearch``, which
is the default ``Searcher``, and it still isn't perfect ;). In fact, we are
planning on replacing it with an A* search when we can work out how.

As such, implementing one of these is a significant undertaking, and a
successful implementation is definitely worth a pull request!

For such a complex module, it has a very simple interface: a single abstract
method ``search(self, ctext: Any) -> SearchResult``, which should accept the
ciphertext, and output the plaintext, with some information on how it got there.
