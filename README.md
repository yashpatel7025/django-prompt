## FYI
* Django-app is deployed on **Microsoft Azure**
* Base URL - > http://django-prompt.centralindia.cloudapp.azure.com
* As discussed with Jordan, project is backend focused and front-end part is not implemented, instead test-cases are written to make sure API logic is correct and desired response is received
* As APIs would not be called by front-end, few validations are added while picking up the request and submitting the feedback.

## API Contracts

**1. Get all feedback request available for user to pickup**

**GET** <em> ```/api/feedback-request/```</em>

```
curl --location --request GET 'http://django-prompt.centralindia.cloudapp.azure.com/api/feedback-request/' \
--header 'Connection: keep-alive' \
--header 'Accept: application/json, text/plain, */*' \
--header 'X-CSRFTOKEN: loX5291kpVZ8oR0pNXOsnZSpRDKr6ZN8fFKEFPzCD53FLL6XIkdUj2YaoSNRtXvr' \
--header 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36' \
--header 'Referer: http://django-prompt.centralindia.cloudapp.azure.com/platform/' \
--header 'Accept-Language: en-US,en;q=0.9' \
--header 'Cookie: _mkto_trk=id:157-GQE-382&token:_mch-azure.com-1620980542106-43300; AMCVS_EA76ADE95776D2EC7F000101%40AdobeOrg=1; AMCV_EA76ADE95776D2EC7F000101%40AdobeOrg=-179204249%7CMCMID%7C76004376289802763820693322583790068238%7CMCAAMLH-1621585342%7C12%7CMCAAMB-1621585847%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1620987742s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C2094946370; LPVID=liMDI3OTMxODFhYTFiMjE4; LPSID-60270350=_4IZCDr-SH6aBZ3oSjCRdQ; csrftoken=8cdQpClO5tSXOlP9ped18bwZHPIMjcfM78tDt24yLSk5Ar5F18uQ3ZeJgE6ZpdTr; sessionid=jbf5wr3ke4hs4bhax07rv960dtwj2bx0'
```

<em>**Sample Response**</em>

```
[
  {
    "pk": 11,
    "essay": {
      "pk": 21,
      "name": "really attention national crime wall (Revision)",
      "uploaded_by": 1,
      "content": "Mother give kind draw wrong put window. Method sister station everybody nice among. There indeed analysis community.",
      "revision_of": 11
    },
    "edited": false,
    "picked_up_by": null,
    "deadline": "2021-07-21T14:52:17.908033Z"
  },
  {
    "pk": 12,
    "essay": {
      "pk": 22,
      "name": "seek herself middle minute structure (Revision)",
      "uploaded_by": 1,
      "content": "Send hot significant end soon. Environment above including their. Financial part common man lot good any contain. Training benefit support best back artist. Laugh design shoulder.",
      "revision_of": 12
    },
    "edited": false,
    "picked_up_by": null,
    "deadline": "2021-07-21T14:52:17.910084Z"
  }
]
```

---

**2. Get detailed feedback request**

**GET** <em>```/api/feedback-request/<pk>/```</em>

```
curl --location --request GET 'http://django-prompt.centralindia.cloudapp.azure.com/api/feedback-request/7' \
--header 'Connection: keep-alive' \
--header 'Accept: application/json, text/plain, */*' \
--header 'X-CSRFTOKEN: loX5291kpVZ8oR0pNXOsnZSpRDKr6ZN8fFKEFPzCD53FLL6XIkdUj2YaoSNRtXvr' \
--header 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36' \
--header 'Referer: http://django-prompt.centralindia.cloudapp.azure.com/platform/' \
--header 'Accept-Language: en-US,en;q=0.9' \
--header 'Cookie: _mkto_trk=id:157-GQE-382&token:_mch-azure.com-1620980542106-43300; AMCVS_EA76ADE95776D2EC7F000101%40AdobeOrg=1; AMCV_EA76ADE95776D2EC7F000101%40AdobeOrg=-179204249%7CMCMID%7C76004376289802763820693322583790068238%7CMCAAMLH-1621585342%7C12%7CMCAAMB-1621585847%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1620987742s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C2094946370; LPVID=liMDI3OTMxODFhYTFiMjE4; LPSID-60270350=_4IZCDr-SH6aBZ3oSjCRdQ; csrftoken=8cdQpClO5tSXOlP9ped18bwZHPIMjcfM78tDt24yLSk5Ar5F18uQ3ZeJgE6ZpdTr; sessionid=jbf5wr3ke4hs4bhax07rv960dtwj2bx0'
```

<em>**Sample Response**</em>

```
{
    "pk": 7,
    "essay": {
        "pk": 17,
        "name": "where relate himself anyone too",
        "uploaded_by": 1,
        "content": "Kind all particularly meeting other present. Else sense appear although ok break. Before choice fish rather stock relationship. Financial mission fast lose natural record. Himself kind rise office must mean every. Agency whose without system democratic my.",
        "revision_of": 16
    },
    "edited": true,
    "picked_up_by": null,
    "deadline": "2021-07-21T14:52:17.901842Z",
    "comments": [],
    "previous_feedback": [
        {
            "pk": 5,
            "essay": 15,
            "edited": true,
            "picked_up_by": null,
            "deadline": "2021-07-21T14:52:17.899218Z",
            "comments": [
                {
                    "id": 1,
                    "feedback_request": 5,
                    "date": "2021-07-21T17:04:21Z",
                    "text": "looks good, just improve the header of the essay"
                },
                {
                    "id": 2,
                    "feedback_request": 5,
                    "date": "2021-07-21T17:05:13Z",
                    "text": "okay header looks good now, nice work, can you also remove the 2nd and 4th paragraph, not necessary"
                }
            ]
        },
        {
            "pk": 6,
            "essay": 16,
            "edited": true,
            "picked_up_by": null,
            "deadline": "2021-07-21T14:52:17.900509Z",
            "comments": [
                {
                    "id": 3,
                    "feedback_request": 6,
                    "date": "2021-07-21T17:06:08Z",
                    "text": "okay, now essay is perfect and completed"
                }
            ]
        }
    ]
}
```

---

**3. Pick up the feedback request.**

**PATCH** <em>```/api/feedback-request/<pk>/```</em>

```
curl --location --request PATCH 'http://django-prompt.centralindia.cloudapp.azure.com/api/feedback-request/8/' \
--header 'Connection: keep-alive' \
--header 'Accept: application/json, text/plain, */*' \
--header 'X-CSRFTOKEN: loX5291kpVZ8oR0pNXOsnZSpRDKr6ZN8fFKEFPzCD53FLL6XIkdUj2YaoSNRtXvr' \
--header 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36' \
--header 'Referer: http://django-prompt.centralindia.cloudapp.azure.com/platform/' \
--header 'Accept-Language: en-US,en;q=0.9' \
--header 'Cookie: _mkto_trk=id:157-GQE-382&token:_mch-azure.com-1620980542106-43300; AMCVS_EA76ADE95776D2EC7F000101%40AdobeOrg=1; AMCV_EA76ADE95776D2EC7F000101%40AdobeOrg=-179204249%7CMCMID%7C76004376289802763820693322583790068238%7CMCAAMLH-1621585342%7C12%7CMCAAMB-1621585847%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1620987742s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C2094946370; LPVID=liMDI3OTMxODFhYTFiMjE4; LPSID-60270350=_4IZCDr-SH6aBZ3oSjCRdQ; csrftoken=8cdQpClO5tSXOlP9ped18bwZHPIMjcfM78tDt24yLSk5Ar5F18uQ3ZeJgE6ZpdTr; sessionid=jbf5wr3ke4hs4bhax07rv960dtwj2bx0'
```

<em>**Sample Response**</em>

```
{
    "message": "feedback request picked up successfully"
}
```
  
<em>**If already picked up by some other editor**</em>
  
  ```
  {
    "message": "request already picked by other editor"
}
  
  ```
  
<em>**if user is not in the assignee list**</em>
  
  ```
  {
    "message": "request can not be picked, you are not assignee of this feedback request"
}
  ```
---
**4. Submit feedback**

**POST** <em> ```/api/feedback-request/comment/```</em>

```
curl --location --request POST 'http://django-prompt.centralindia.cloudapp.azure.com/api/feedback-request/comment/' \
--header 'Connection: keep-alive' \
--header 'Accept: application/json, text/plain, */*' \
--header 'X-CSRFTOKEN: loX5291kpVZ8oR0pNXOsnZSpRDKr6ZN8fFKEFPzCD53FLL6XIkdUj2YaoSNRtXvr' \
--header 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36' \
--header 'Referer: http://django-prompt.centralindia.cloudapp.azure.com/platform/' \
--header 'Accept-Language: en-US,en;q=0.9' \
--header 'Cookie: _mkto_trk=id:157-GQE-382&token:_mch-azure.com-1620980542106-43300; AMCVS_EA76ADE95776D2EC7F000101%40AdobeOrg=1; AMCV_EA76ADE95776D2EC7F000101%40AdobeOrg=-179204249%7CMCMID%7C76004376289802763820693322583790068238%7CMCAAMLH-1621585342%7C12%7CMCAAMB-1621585847%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1620987742s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C2094946370; LPVID=liMDI3OTMxODFhYTFiMjE4; LPSID-60270350=_4IZCDr-SH6aBZ3oSjCRdQ; csrftoken=8cdQpClO5tSXOlP9ped18bwZHPIMjcfM78tDt24yLSk5Ar5F18uQ3ZeJgE6ZpdTr; sessionid=jbf5wr3ke4hs4bhax07rv960dtwj2bx0' \
--header 'Content-Type: application/json' \
--data-raw '{
    "feedback_request":8,
    "text": "essay looks good, just change footer and 5th paragraph"
}'
```
<em>**Sample Response**</em>

```
{
    "message": "feedback submitted"
}
```

<em>**if not picked up by user or already pickedup by some other editor**</em>
 
  ```
  {
    "errors": {
        "non_field_errors": [
            "request is not picked by you or might have picked by some other editor"
        ]
    }
}
  ```

---

### Contact if need any help

- **Email**:- yashpatel7025@gmail.com
- **Call**: 7021875166, **Whatsapp**:9730039951

---
---
