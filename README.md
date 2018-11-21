# About

UnnaturalCode is a system with the purpose of augmenting the compiler's own
syntax error location strategies. It is designed to assist the developer in
locating syntax errors in their software. For more information, please consult
the [UnnaturalCode paper](http://webdocs.cs.ualberta.ca/~joshua2/syntax.pdf) (preprint).

* [Video Demo](https://www.youtube.com/watch?v=mIMpfh7rDEk)
* [Slides](http://webdocs.cs.ualberta.ca/~joshua2/syntax_presentation.pdf)
* [Installation](INSTALL.md)
* [About the Authors](AUTHORS.md)

UnnaturalCode should be considered proof-of-concept quality software. The
primary author of UnnaturalCode, Hazel Victoria Campbell can be reached at <hazel.campbell@ualberta.ca>.

# Install

Clone this repository with the recursive option:

    git clone --recursive https://github.com/orezpraw/unnaturalcode.git

Alternatively, clone this repository, then initialize `git-submodules`.

    git submodule update --init

This will also clone [MITLM].

[MITLM]: https://github.com/orezpraw/MIT-Language-Modeling-Toolkit/tree/267325017f60dee86caacd5b207eacdc50a3fc32

> **macOS**: MITLM requires gfortran, which must be installed before
> running `pip install`.
>
>     brew install gcc
>
> Then, prior to the pip install, set the `LIBRARY_PATH` as appropriate:
>
>     export LIBRARY_PATH="$(dirname $(brew list gcc | grep libgfortran.a | tail -1)):$LIBRARY_PATH"

Create a virtualenv (optional), then:

    pip install -e .

Must set the PATH for the following compilers:

JavaScript:

- Babel
- V8
- EsLint
- JavaScriptCore

Execute the following for each compiler:

    export PATH=/YOUR_LOCATION_OF_FILE/:$PATH

An example for Babel:

    export PATH=/home/dhvani/node_modules/.bin:$PATH
    
Requirement for Java:

Path to ecj-4.7.jar (Eclipse compiler standalone jar) must be set in check_eclipse_syntax.py

# Use

To start the HTTP server:

    python -m unnaturalcode.http

# Licensing

Assume that UnnaturalCode is licensed under the [AGPL3+](LICENSE) unless otherwise
specified.

&copy; 2010-2012 Abram Hindle, Prem Devanbu, Earl T. Barr, Daryl Posnett

&copy; 2012-2014 Joshua Charles Campbell, Abram Hindle, Alex Wilson

UnnaturalCode is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

UnnaturalCode is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
details.

You should have received a copy of the GNU Affero General Public License along
with UnnaturalCode.  If not, see <http://www.gnu.org/licenses/>.

# Academic Use

Now we aren't going to impose any extra requirements, but we ask kindly if you
are using this academically that you should consider citing our relevant work:

    @InProceedings{campbellMSR2014,
      author =       {Joshua Charles Campbell and Abram Hindle and José Nelson Amaral},
      title =        {{Syntax Errors Just Aren’t Natural: Improving Error Reporting with Language Models}},
      booktitle = {Proceedings of the 11th Working Conference on Mining Software Repositories},
      year =      {2014},
      pages =     {10}
    }

