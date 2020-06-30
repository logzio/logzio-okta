from ruamel.yaml import YAML
LOGSTASH_CONF_PATH = "./pipeline/logstash.conf"
MAX_TENANTS = 50
VALID_DOMAINS = ('okta.com', 'oktapreview.com', 'okta-emea.com')
error_msg = "Please run 'docker stop Okta' and rerun the container with a valid tenants-credentials.yml file."

def _build_logstash_config():
    yaml = YAML()
    logstash_input = ""
    line_counter = 2
    with open("tenants-credentials.yml", "r") as tenants_yml:
        try:
            config_dict = yaml.load(tenants_yml)
        except YAML.scanner.ScannerError as exc:
            raise Exception("Your YAML file is invalid. Make sure you are not missing any 'okta_api_key' and that you don't have any redundant spaces or tabs.\n %s" % error_msg)

    if str(config_dict).count('okta_api_key') > MAX_TENANTS:
        raise Exception("You have exceeded the maximum number of tenants. Please insert up to 50 tenants.")

    for tenant in config_dict["tenants_credentials"]:
        tenant_dict = _add_tenant(tenant, line_counter)
        logstash_input = tenant_dict + logstash_input
        line_counter += 2

    logstash_config = open(LOGSTASH_CONF_PATH, "r+")
    logstash_output = logstash_config.read()
    logstash_config.seek(0)
    logstash_config.write(logstash_input)
    logstash_config.write(logstash_output)
    logstash_config.seek(0)
    logstash_config.close()
    tenants_yml.close()


def _add_tenant(tenant, line):
    try:
        okta_api_key = tenant["okta_api_key"]
        okta_domain = tenant["okta_domain"]
        if not okta_domain.endswith(VALID_DOMAINS):
            raise Exception("Your Okta domain in line %d is invalid.\n %s" % (line, error_msg))
        tenant_dict = "input {\n okta_system_log {\n schedule => {every => '30s'}\n limit => 1000\n auth_token_key => '%s'\n hostname =>  '%s'\n }\n }\n" % (okta_api_key, okta_domain)
        return tenant_dict
    except Exception:
        raise Exception("The tenant in line %d is missing an Okta domain.\n %s" % (line, error_msg))


_build_logstash_config()
