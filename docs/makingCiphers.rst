How to add a cipher
===================

Ciphey relies on ciphers, and as much we have made it as easy as
possible for you to add a cipher to Ciphey.

Decoders vs Crackers
--------------------

An encoding is defined as: > Any form of encryption that doesn’t use a
key So for example, Base64 doesn’t require a key. But caesar cipher
requires a key.

Decoders are located in ``ciphey/basemods/Decoders`` Crackers are
located in ``ciphey/basemods/Crackrs`` and also in cipheyCore. We’ll
talk more about this later.

We’ll walk through adding a decoder first.

Adding a decoder
----------------

.. code:: python

   from typing import Optional, Dict, List

   from ciphey.iface import ParamSpec, Config, T, U, Decoder, registry


   @registry.register_multi((str, str), (bytes, bytes))
   class YOURCLASSNAMEHERE(Decoder):
       def decode(self, ctext: T) -> Optional[U]:
           """Write the code that decodes here
           ctext -> the input to the function
           returns string
       """

       @staticmethod
       def priority() -> float:
           """How often is this seen in a CTF out of 1
           Returns float
           """

       def __init__(self, config: Config):
           super().__init__(config)

       @staticmethod
       def getParams() -> Optional[Dict[str, ParamSpec]]:
           """The parameters this returns"""
           pass

       @staticmethod
       def getTarget() -> str:
           """The name of the decoding ussed
           returns string
           """

Copy this file into ``ciphey/basemods/Decoders`` and save it as a
template. For example, let’s try to add a decoder for the first letter
of every word.

We need to come up with a succint name for it, so let’s call it
“firstLetter.py”

Now, the first thing we have to do is rename the class.

::

   class YOURCLASSNAMEHERE(Decoder):

Let’s rename it to firstLetter:

::

   class FirstLetter(Decoder):

Now, to write the decode function. This is the part that you created and
work on! I would suggest building it locally, in a seperate file and
testing it before integrating with Ciphey.

For our purposes, let’s build the first letter function.

.. code:: python

   def decode(self, ctext: T) -> Optional[U]:
       """Write the code that decodes here
       ctext -> the input to the function
       returns string
       """
       ret = []
       for word in ctext.split(" "):
           # for each word in the ctext, append the first letter
           # of that word to a list
           ret.append[word[0]]
       # and then return the list as a single word
       return ''.join(ret)
       

Don’t forget to comment it ;)

Now, the next function we need to change is priority. **Guess** how
often it’ll appear. For instance, we see Base64 appear all the time. But
we almost never see First Letter of every word appear.

So the priority will be very low. Let’s set it to an arbitrarily low
number, such as 0.05.

.. code:: python

   @staticmethod
   def priority() -> float:
       """How often is this seen in a CTF out of 1
       Returns float
       """
       return 0.05

The next function will be the defParams() function. Only use this
function if your decoder has to return paraemters. Most of the time, it
will not.

The final function is ``getTarget()``.

.. code:: python

   @staticmethod
   def getTarget() -> str:
       """The name of the decoding ussed
       returns string
       """
       return "firtLetter"
       ```
       
   This function describes _what_ the decoder is trying to solve. In our case, let\'s name it firstLetter.

   Our full function now looks like:

.. code:: python

   from typing import Optional, Dict, List

   from ciphey.iface import ParamSpec, Config, T, U, Decoder, registry


   @registry.register_multi((str, str), (bytes, bytes))
   class FirstLetter(Decoder):
       @staticmethod
       def decode(self, ctext: T) -> Optional[U]:
           """Write the code that decodes here
           ctext -> the input to the function
           returns string
           """
           ret = []
           for word in ctext.split(" "):
               # for each word in the ctext, append the first letter
               # of that word to a list
               ret.append[word[0]]
           # and then return the list as a single word
           return ''.join(ret)
       @staticmethod
       def priority() -> float:
           """How often is this seen in a CTF out of 1
           Returns float
           """
           return 0.05
           
       @staticmethod
       def getParams() -> Optional[Dict[str, ParamSpec]]:
           """The parameters this returns"""
           pass
       
       @staticmethod
       def getTarget() -> str:
           """The name of the decoding ussed
           returns string
           """
           return "firtLetter"


