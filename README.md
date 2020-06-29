# logzio-okta

To ship Okta logs,
you'll deploy a Docker container
to collect the logs and forward them to Logz.io.

#### Configuration

**Before you begin, you'll need**:
Okta administrator privileges

<div class="tasklist">

#### Get the API token and domain from Okta

In the Okta developer console,
navigate to **API > Tokens**.
Create a token and paste it in your text editor.

![Create Okta API token](https://dytvr9ot2sszz.cloudfront.net/logz-docs/log-shipping/okta-create-token.png)

Click the **Authorization Servers** tab.
Copy your Okta domain from the **Issuer URI** column,
and paste it in your text editor. In the following example, you'd have copied "dev-123456.okta.com".

![Okta URL](https://dytvr9ot2sszz.cloudfront.net/logz-docs/log-shipping/okta-issuer-uri.png)

#### Pull the Docker image

Download the logzio/logzio-okta image.

```shell
docker pull logzio/logzio-okta
```

#### Run the Docker image

Build your tenants-credentials.yml:

``` 
touch tenants-credentials.yml
```

Insert your tenants credentials in the following format:
```
tenants_credentials:
    - okta_api_key: <<OKTA-API-KEY>
      okta_domain: <<OKTA-DOMAIN>>
```

For multiple tenants, add your okta API and domain for each tenant as the following example:
```
tenants_credentials:
    - okta_api_key: 123456a
      okta_domain: logzio-dev-123.okta.com
    - okta_api_key: 123456b
      okta_domain: logzio-dev-123.okta.com
    - okta_api_key: 123456c
      okta_domain: logzio-dev-123.oktapreview.com
```
** Note that 'YAML' files are sensitive to spaces and tabs, then keep this structure accurate.


#### Parameters
For every tenant replace the parameters by:  

| Parameter | Description |
|---|---|
| OKTA_API_KEY <span class="required-param"></span> | The Okta API key you copied in step 1. |
| OKTA_DOMAIN <span class="required-param"></span> | Insert your Okta domain that you copied in step 1 from the issuer URI column. For example: logzio-dev-123.okta.com, logzio-dev-123.oktapreview.com|

Save the file on your working directory (where you're running the docker from) and run:

```shell
docker run \
--detach \
--restart always \
--name Okta \
--env MULTI_TENANTS=<<SHIPPING-TOKEN>> \
--env LOGZIO_LISTENER_HOST=<<LISTENER-HOST>> \
-v $(pwd)/tenants-credentials.yml:/usr/share/logstash/tenants-credentials.yml \
-t logzio/logzio-okta
```

#### Parameters

| Parameter | Description |
|---|---|
| LOGZIO_TOKEN <span class="required-param"></span> | Your Logz.io account [token]((https://app.logz.io/#/dashboard/settings/general)). |
| LOGZIO_LISTENER_HOST <span class="required-param"></span> | Logz.io [listener URL](https://docs.logz.io/user-guide/accounts/account-region.html) to ship the logs to (for example, listener.logz.io). |


#### Check Logz.io for your logs

Give your logs some time to get from your system to ours,
and then open [Kibana](https://app.logz.io/#/dashboard/kibana).


## Versions

0.1.0:
* Sending logs from multiple Okta tenants
* Sending logs with from every kind of okta domain (not limited to 'okta.com')

0.0.2:
* Sending logs from Okta tenants

</div>

