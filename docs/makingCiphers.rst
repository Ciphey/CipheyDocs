How to add a cipher
===================

TODO:
- [ ] convert to Octal template
- [ ] Mention __init__.py
- [ ] Mention [str, bytes]

Ciphey relies on ciphers, and as much we have made it as easy as
possible for you to add a cipher to Ciphey.

Decoders vs Crackers
--------------------

An encoding is defined as: "Any form of encryption that doesn’t use a
key". Also to note, decodings take significantly less time than a cracker. So for example, Base64 doesn’t require a key. But caesar cipher
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
       Returns float``
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

Crackers
--------
Now we'll walk through how to build a cracker.

We prefer to use CipheyCore for ciphers. This is because the C++ core is much, much faster than any Python implementations. The location for ciphers in CipheyCore is ``CipheyCore/src/ciphers/``. 

All you have to do is write efficient C++ code. Much harder than it sounds! Maybe sure your potential keyspace can't become crazy big. 

Use a library such as SWIG to connect the C++ code to Python. 

Here's an example of the Python class that connects the C++ to the Cracker interface. It's rather similar to the Decoder interface, so there isn't as much information provided.

.. code:: python

        from distutils import util
        from typing import Optional, Dict, Union, Set, List

        from loguru import logger
        import ciphey
        import cipheycore

        from ciphey.iface import ParamSpec, CrackResult, T, CrackInfo, registry

        @registry.register
        class Caesar(ciphey.iface.Cracker[str]):
            def getInfo(self, ctext: T) -> CrackInfo:
                # Information which can help crack the cipher
                analysis = self.cache.get_or_update(
                    ctext,
                    "cipheycore::simple_analysis",
                    lambda: cipheycore.analyse_string(ctext),
                )

                return CrackInfo(
                    success_likelihood=cipheycore.caesar_detect(analysis, self.expected),
                    # TODO: actually calculate runtimes
                    success_runtime=1e-4,
                    failure_runtime=1e-4,
                )

            @staticmethod
            def getTarget() -> str:
                return "caesar"

            def attemptCrack(self, ctext: str) -> List[CrackResult]:
                logger.debug("Trying caesar cipher")
                # Convert it to lower case
                #
                # TODO: handle different alphabets
                if self.lower:
                    message = ctext.lower()
                else:
                    message = ctext

                logger.trace("Beginning cipheycore simple analysis")

                # Hand it off to the core
                analysis = self.cache.get_or_update(
                    ctext,
                    "cipheycore::simple_analysis",
                    lambda: cipheycore.analyse_string(message),
                )
                logger.trace("Beginning cipheycore::caesar")
                possible_keys = cipheycore.caesar_crack(
                    analysis, self.expected, self.group, True, self.p_value
                )
                n_candidates = len(possible_keys)
                logger.debug(f"Caesar returned {n_candidates} candidates")

                candidates = []

                for candidate in possible_keys:
                    translated = cipheycore.caesar_decrypt(message, candidate.key, self.group)
                    candidates.append(CrackResult(value=translated, key_info=candidate.key))

                return candidates



            @staticmethod
            def getParams() -> Optional[Dict[str, ParamSpec]]:
                return {
                    "expected": ciphey.iface.ParamSpec(
                        desc="The expected distribution of the plaintext",
                        req=False,
                        config_ref=["default_dist"],
                    ),
                    "group": ciphey.iface.ParamSpec(
                        desc="An ordered sequence of chars that make up the caesar cipher alphabet",
                        req=False,
                        default="abcdefghijklmnopqrstuvwxyz",
                    ),
                    "lower": ciphey.iface.ParamSpec(
                        desc="Whether or not the ciphertext should be converted to lowercase first",
                        req=False,
                        default=True,
                    ),
                    "p_value": ciphey.iface.ParamSpec(
                        desc="The p-value to use for standard frequency analysis",
                        req=False,
                        default=0.1,
                    )
                    # TODO: add "filter" param
                }

            @staticmethod
            def scoreUtility() -> float:
                return 1.5

            def __init__(self, config: ciphey.iface.Config):
                super().__init__(config)
                self.lower: Union[str, bool] = self._params()["lower"]
                if type(self.lower) != bool:
                    self.lower = util.strtobool(self.lower)
                self.group = list(self._params()["group"])
                self.expected = config.get_resource(self._params()["expected"])
                self.cache = config.cache
                self.p_value = self._params()["p_value"]
                
If you need help with this, create a GitHub issue or contact us on Discord at discord.ciphey.online.
