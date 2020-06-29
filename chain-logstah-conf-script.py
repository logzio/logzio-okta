from ruamel.yaml import YAML
LOGSTASH_CONF_PATH = "./pipeline/logstash.conf"

def _build_logstash_config():
    yaml = YAML()
    logstash_input = ""

    with open("tenants-credentials.yml", "r") as tenants_yml:
        config_dict = yaml.load(tenants_yml)
    for tenant in config_dict["tenants_credentials"]:
        tenant_dict = _add_tenant(tenant)
        logstash_input = tenant_dict + logstash_input
    logstash_config = open(LOGSTASH_CONF_PATH, "r+")
    logstash_output = logstash_config.read()
    logstash_config.seek(0)
    logstash_config.write(logstash_input)
    logstash_config.write(logstash_output)
    logstash_config.seek(0)
    logstash_config.close()
    tenants_yml.close()


def _add_tenant(tenant):
    okta_api_key = tenant["okta_api_key"]
    okta_uri = tenant["okta_domain"]
    tenant_dict = "input {\n okta_system_log {\n schedule => {every => '30s'}\n limit => 1000\n auth_token_key => '%s'\n hostname =>  '%s'\n }\n }\n" % (okta_api_key, okta_uri)
    return tenant_dict

_build_logstash_config()
