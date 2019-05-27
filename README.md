# json-inherited-attributes

Create json key-value pairs based on an inheritance model to help
keep file contents relatively simple to maintain.

The parser will continue reading additions to a chain of inheritance
until it encounters a *dead end* (where no more children objects are
found to continue parsing) that is nested at least at the defined
`MINIMUM_DEPTH` (default 1). In the example below, the `sedan` and
`hatchback` trims are dead-ends and will thus end the parsing/inheritance
chain.

The only key values that aren't overwritten are 'include' directives
for the sake of referencing by a follow-up parser.

For help regarding command line arguments for the parser:

    python3 ./parse.py -h

### Example Usage

    python3 ./parse.py input/test-input.json output/test-output.json
    
Takes the following input file, styled based on inheritance of attributes...

    {
      "mazda": {
        "make": "mazda",
        "mazda-3": {
          "model": "mazda-3",
          "variants": ["base", "select", "preferred", "premium"],
          "trim": {
            "sedan": {},
            "hatchback": {
              "six-cylinder-variant": "premium"
            }
          }
        }
      }
    }

And outputs a relatively flat json object:

    {
      "mazda_mazda-3_trim_hatchback": {
        "make": "mazda",
        "model": "mazda-3",
        "six-cylinder-variant": "premium",
        "variants": [
          "base",
          "select",
          "preferred",
          "premium"
        ]
      },
      "mazda_mazda-3_trim_sedan": {
        "make": "mazda",
        "model": "mazda-3",
        "variants": [
          "base",
          "select",
          "preferred",
          "premium"
        ]
      }
    }