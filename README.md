# logzio-okta

To ship Okta logs,
you'll deploy a Docker container
to collect the logs and forward them to Logz.io using Logstash.
You can send logs from multiple Okta tenants and any okta domain.

#### Configuration

**Before you begin, you'll need**:
Okta administrator privileges

<div class="tasklist">

#### Get the API token and Okta domain from Okta

In the Okta developer console,
navigate to **API > Tokens**.
Create a token and paste it in your text editor.

![Create Okta API token](https://dytvr9ot2sszz.cloudfront.net/logz-docs/log-shipping/okta-create-token.png)

Click the **Authorization Servers** tab.
Copy your Okta domain from the **Issuer URI** column,
and paste it in your text editor. In the following example, you'd have copied "dev-123456.okta.com".

![Okta URL](https://dytvr9ot2sszz.cloudfront.net/logz-docs/log-shipping/okta-issuer-uri.png)

#### Build your tenants-credentials.yml
To create the file run the following command as root and then open the file in your text editor:

``` 
mkdir /etc/logzio-okta && touch /etc/logzio-okta/tenants-credentials.yml
```

#### Insert your tenants credentials in the following format:
```
tenants_credentials:
    - okta_api_key: <<OKTA-API-KEY>
      okta_domain: <<OKTA-DOMAIN>>
```

This shipper supports up to 50 tenants. For multiple tenants, add your Okta API key and domain for each tenant.  
See the following example:
```
tenants_credentials:
    - okta_api_key: 123456a
      okta_domain: logzio-dev-123.okta.com
    - okta_api_key: 123456b
      okta_domain: logzio-dev-123.okta.com
    - okta_api_key: 123456c
      okta_domain: logzio-dev-123.oktapreview.com
```
** Note that YAML files are sensitive to spaces and tabs. We recommend using a YAML validator to make sure that the file structure is correct. 


#### Parameters
For every tenant replace the parameters by:  

| Parameter | Description |
|---|---|
| OKTA_API_KEY <span class="required-param"></span> | The Okta API key you copied in step 1. |
| OKTA_DOMAIN <span class="required-param"></span> | Insert your Okta domain that you copied in step 1 from the issuer URI column. Supports these [Okta domains](https://developer.okta.com/docs/guides/find-your-domain/findorg/): example.oktapreview.com, example.okta.com, example.okta-emea.com |

To filter by tenants the logs have the field 'tenant_name'.  

Save the file on your working directory (where you're running the docker from).

#### Pull the Docker image

Download the logzio/logzio-okta image.

```shell
docker pull logzio/logzio-okta
```

#### Run the Docker image

Replace the placeholders in the code sample below before running it. Then run:

```shell
docker run \
--restart always \
--name Okta \
--env LOGZIO_TOKEN=<<SHIPPING-TOKEN>> \
--env LOGZIO_LISTENER_HOST=<<LISTENER-HOST>> \
-v /etc/logzio-okta/tenants-credentials.yml:/usr/share/logstash/tenants-credentials.yml \
-t logzio/logzio-okta
```
For Mac users: To fix issues with mounting files from root directory please add the path ‘/etc/logzio-okta’ to your Docker File Sharing.
Click [here](https://medium.com/effy-tech/fixing-the-var-folders-error-in-docker-for-mac-v2-2-3-2a40e776132d) for a guide on how to fix this issue - using docker desktop or manually edit your Docker configuration file.
For more information about mounting files from root directory click [here](https://docs.docker.com/docker-for-mac/osxfs/#namespaces).

##### Parameters

| Parameter | Description |
|---|---|
| LOGZIO_TOKEN <span class="required-param"></span> | Your Logz.io account [token]((https://app.logz.io/#/dashboard/settings/general)). |
| LOGZIO_LISTENER_HOST <span class="required-param"></span> | Logz.io [listener URL](https://docs.logz.io/user-guide/accounts/account-region.html) to ship the logs to (for example, listener.logz.io). |


##### Check Logz.io for your logs

Give your logs some time to get from your system to ours,
and then open [Kibana](https://app.logz.io/#/dashboard/kibana).

## Versions

0.1.1:
* Added 'tenant_name' field to the logs

0.1.0:
* Sending logs from multiple Okta tenants
* Sending logs with from every kind of okta domain (not limited to 'okta.com')
* Note that 'okta_api_key' and 'okta_domain' are now being set in 'tenants-credentials.yml' and no longer as environment parameters.

0.0.2:
* Sending logs from Okta tenants

</div>

