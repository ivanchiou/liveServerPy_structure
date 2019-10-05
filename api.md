# Server API for Live System
**V.0.0.1**

By Ivan Chiou

Oct. 5, 2019

Revisions
-----------
The version will represent as three part: x.x.x 

* First part is major protocol version number. It will be changed when it has flow or behavior changes and incompatible with the backward version

* Second part is minor protocol version number. It will be changed when definition or behavior changes but it still compatible with the backward version

* Third part is document version number for this protocol version. It will changed if it is just enhanced the document without change the protocol.

| Version | Revised Date | Reviser    | Revised Content |
|---------|--------------|------------|-----------------|
| 0.0.1   | Oct. 5, 2019 | Ivan Chiou | Draft           |

# 1. Overview

This API is designed to provide the access for other services to manager , create, and query products in basket. It is a RESTful API based on standard HTTP request/response with UTF-8 encoded JSON data for communication.

##1.1 Design Convention

**Request Format**

The request is based on standard HTTP request with standard HTTP 
method like GET or POST. The format of request is as following:

| https://&lt;host>/api/&lt;version>/&lt;resourcePath>?&lt;modifier> |
|-----------------------------------------------------------------------|


**Definition**

| Arguments    | Description                                                                                                                                                                   |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Host         | This is a host domain name of this api. (Ex: example.com)                                                                                                                     |
| Version      | This is the major protocol version (Ex: v1, v2, v3…)                                                                                                                          |
| ResourcePath | This is a path combined with a chain of individual data entities including its target ID(Ex: /organizations/&lt;organization-id>/licenses/&lt;license-id>) to handle some particular action of the request |
| Modifier     | This is use to provide the filter(s) or modifier(s) which need to be applied on the reply data. This is also useful to provide the limited information when querying a large data.  |


**Options of Modifiers**


| Modifier   | Descriptions                                                                                                                                                                             |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pretty     | The result will reply as compact format by default. However, it can append this value to make API reply the pretty format with proper line breaking and indentation to make it readable. |
| Opt_fields | This does not mean a specific parameter. This option allows you to list a set of modifiers that the API should use it as extra condition to return for the objects.                                                                           |

**Response Format**

The response format for all requests is a JSON object.

The API will response the request with JSON object with standard HTTP status code to represent the result of the request.

If there is no any item in a response, it is not an error. A empty JSON object/array should be returned.

Empty response example
```javascript
{}
```

**Request Example**

```curl
curl –u “https://xxx.xxx.xxx.xxx/api/v1/products/1/?pretty=true” 
```


**Response Example**

 **HTTP/1.1 200**
```javascript
{
  "goodId": 1,
  "name": "Samsung Galaxy S10+ 6.4吋智慧型手機 8G/128G",
  "price": 100,
  "promoMsg": "30% OFF",
  "image": "https://ehs-shop.tyson711.now.sh/static/images/470x600-02.jpg",
  "url": "",
  "description": "This is description",
  "styleInfo": [
    {
      "value": "a0015",
      "title": "黑色",
      "quantity": 10
    },
    {
      "value": "a0016",
      "title": "白色",
      "quantity": 6
    }
  ]
}
```
##1.2 Rules for token, ID and name

### access_token
* A User Identifier to checkout products in basket

### product ID
* Uppercase and lowercase Latin letters (a–z, A–Z) (ASCII: 65–90, 97–122)
* Digits 0 to 9 (ASCII: 48–57)
* Special characters: +-.@_ (ASCII: 43, 45,46, 64,95)
* The maximum length is 64.

### Order ID
* Uppercase and lowercase Latin letters (a–z, A–Z) (ASCII: 65–90, 97–122)
* Digits 0 to 9 (ASCII: 48–57)
* Special characters: +-.@_ (ASCII: 43, 45,46, 64,95)
* The maximum length is 64.


## 1.3 Request
### Method Summary

| URL                          | HTTP Method | Description                                                            |
|------------------------------|-------------|------------------------------------------------------------------------|
| /products                                      | GET    | Get all products of this set of APIs.                                      |
| /products/&lt;products-id>            | GET    | Get specific product of this set of APIs.                                     |
| /basket                                    |POST | Add products to basket                          


# 2. Methods Details

This section describes the methods provided by this API. 

## 2.1. General
 
### 2.1.1. Get all products of this set of APIs.

#### Request Method

| GET | /products |
|-----|-----------------|



#### Request Example

```curl
curl –u "https://xxx.xxx.xxx/api/v1/products" \
-X GET \
```

#### Response Data

| Response Code        | Description            |
|----------------------|------------------------|
| Normal Response code | 200                    |
| Errors Response code | 404-01, 405-01, 420-01, 420-02 |

| Parameter        | Type   | Description                       |
|------------------|--------|-----------------------------------|
| category      | String | the category name of products.                   |
| cateId | Integer | the category id of products.              |
| data           | JSON   | the product details including goodId, name, price, promoMsg, image, url, description, styleInfo |



#### Response Example
Here return version number for both API and Software.

**HTTP/1.1 200**
```javascript
{
  [
    {
      "category": "時尚",
      "cateId": 11,
      "data": [
        {
          "goodId": 0,
          "name": "Samsung Galaxy S10+ 6.4吋智慧型手機 8G/128G",
          "price": 0,
          "promoMsg": "30% OFF",
          "image": "https://ehs-shop.tyson711.now.sh/static/images/470x600-01.jpg",
          "url": "",
          "description": "This is description",
          "styleInfo": [
            {
              "value": "a0015",
              "title": "黑色",
              "quantity": 10
            },
            {
              "value": "a0016",
              "title": "白色",
              "quantity": 6
            }
          ]
        },
        {
          "goodId": 2,
          "name": "Samsung Galaxy S10+ 6.4吋智慧型手機 8G/128G",
          "price": 200,
          "promoMsg": "30% OFF",
          "image": "https://ehs-shop.tyson711.now.sh/static/images/470x600-03.jpg",
          "url": "",
          "description": "This is description",
          "styleInfo": [
            {
              "value": "a0015",
              "title": "黑色",
              "quantity": 10
            },
            {
              "value": "a0016",
              "title": "白色",
              "quantity": 6
            }
          ]
        }
    }
  ]
}

```

**HTTP/1.1 420**
```javascript
{
    "errors": {
        "code": "420-01",
        "message": "Method Failure. The method 'xxx' has some program errors"
    }
}
```

# 4. Errors

**HTTP Response Code**

| Code | Description                                                                                                                |
|------|----------------------------------------------------------------------------------------------------------------------------|
| 200  | OK This represents the data was requested successfully.                                                                    |
| 201  | Created This represents the object can be retrieved and created.                                                           |
| 204  | No Content This represents the data has no response body.                                                                  |
| 400  | Bad Request This represents the syntax error. It may occurs when there are malformed or missing parameters in the request. |
| 401  | Unauthorized This represents the authentication failed. It may occurs when the API_KEY is incorrect or not provided.       |
| 403  | Forbidden This represents the request does not have privileges to access the data.                                         |
| 404  | Not Found This represents the request target does not existed.                                                             |
| 405  | Method Not Allowed This represents the request method are not allowed.                                                     |
| 406  | Not Acceptable This represents the server doesn't find any content following the criteria given by the user agent.         |
| 409  | Conflict This represents the request conflict(duplicated or insert failed) with current state of server.                   |
| 420  | Method Failure This represents the request method is failed because of some program errors                                 |
| 429  | Too Many Requests This represents the clients has sent too many requests over the server's loading.                        |



**Errors Code and Message**

|    Code      |    Message                                                                 |
|--------------|----------------------------------------------------------------------------|
|    400-01    |    Syntax Error. The syntax is not   correct or missing some parameters    |
