![PickPocketAndroid](intrepid-logo.png)
# PickPocket Backend - Winter 2017

## Overview of Project:

The project is structured as a series of AWS Lambda functions with a DynamoDB database to store information. The lambda functions can be deployed using AWS API Gateway to allow for the remote access of the endpoints. Initially, this was done in a very manual process. There is now a set of scripts built around Amazon Cloud Formation to allow for a quick deployment of the system to any AWS account.

Currently the database and SNS integration still need to be configured manually.

* [Deploying](#deploying) - The functions can be copy and pasted manually to aws or the shell script can handle their generation automatically.
* [Functions](#functions) - Create a UI that allows you to play a one-way Mastermind game against a computer opponent.
* [Previous Guesses](#previous-guesses) - Add a list of previous guesses to the UI to make it easier to remember what you’ve already guessed.
* [Networking](#networking) - Add a networking class that allows you to crack a remote lock using an API.

## Deploying

To deploy automatically, first configure the functions in `config.json` similar to below:

```Javascript
{
  "functions" : [
    {
      "function":"FetchUsers.py",
      "api_path":"users",
      "method":"GET"
    },
    {
      "function":"CreateUserBasic.py",
      "api_path":"users",
      "method":"POST"
    },
    {
      "function":"PickLockUrl.py",
      "api_path":"pick/{victim}",
      "method":"POST"
    }
  ]
}
```

Where:
* `function` is the name of the python file
* `api_path` is the route that will be used in the api gateway
* `method` is the type of request the lambda function will correspond to (ex: GET, POST)

Once that is done call `deploy.sh` with the name you would like to use for the stack:

```Bash
  ./deploy.sh STACKNAME
```

## Functions

Below is a quick overview of the different lambda functions in this repository, for more information please refer to the individual files:

* `FetchUsers` - Returns a list of the userIDs of every person in the database along with the length of their combination.
* `CreateUserBasic` - Supply a userId, DisplayName, and Combination, returns an error if username taken, otherwise returns success and a token.
* `PickPocketUrl` - Provide a UserId to pick, the token of the current user, and a combination guess to attempt to pick the lock of another user.
* `UpdateDisplayName` - Allows a user to change their display name. UserId cannot be changed.
* `EditCombination` - Provide a token and new combination to change the lock associated with that user.
* `PickPocket` This is a deprecated function and should not be used anymore. It does not require the token to pick a user.

## Quirks
When you first run the deployment script you may receive an error that there is no file `deploy.json`. This is due to a quick hack that first deletes the existing file if its there before running `concat_files.py.` It will hopefully be fixed in future updates. 
