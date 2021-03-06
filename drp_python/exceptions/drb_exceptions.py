# Copyright 2018 Cable Television Laboratories, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class DrbError(Exception):
    """Base class for drb-exceptions in this module."""

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __str__(self):
        return 'Error on ' + self.expression + ':  ' + self.message


class ActionError(DrbError):
    """Exception raised for authorization errors.
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, action, message):
        DrbError.__init__(self, action, message)


class AlreadyExistsError(DrbError):
    """Exception raised trying to create an existing resource.
       Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self, key, message):
        DrbError.__init__(self, key, message)


class NotFoundError(DrbError):
    """Exception raised when a resource doesn't exist errors.
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self, key, message):
        DrbError.__init__(self, key, message)
