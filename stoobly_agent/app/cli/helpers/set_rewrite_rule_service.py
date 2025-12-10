from typing import List, Optional

from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.rewrite_rule import ParameterRule, RewriteRule, UrlRule


def _select_parameter_rule(kwargs: dict) -> Optional[dict]:
    """Select parameter rule from kwargs if all required fields are present."""
    if kwargs.get('name') is None or kwargs.get('value') is None or kwargs.get('type') is None:
        return None

    return {
        'modes': list(kwargs['mode']),
        'name': kwargs['name'],
        'value': kwargs['value'],
        'type': kwargs['type'],
    }


def _select_url_rule(kwargs: dict) -> Optional[dict]:
    """Select URL rule from kwargs if any URL fields are present."""
    if (kwargs.get('scheme') is None and kwargs.get('hostname') is None and 
        kwargs.get('port') is None and kwargs.get('path') is None):
        return None

    return {
        'hostname': kwargs.get('hostname'),
        'modes': list(kwargs['mode']),
        'path': kwargs.get('path'),
        'port': kwargs.get('port'),
        'scheme': kwargs.get('scheme'),
    }


def set_rewrite_rule(project_id: str, **kwargs) -> None:
    """
    Set or update a rewrite rule for a project.
    
    Args:
        project_id: The project ID to set the rewrite rule for
        **kwargs: Keyword arguments containing:
            - pattern: URL pattern to match (required)
            - method: HTTP methods (required, multiple)
            - mode: Modes to apply rule to (required, multiple)
            - name: Parameter name (optional, for parameter rules)
            - value: Parameter value (optional, for parameter rules)
            - type: Parameter type (optional, for parameter rules)
            - scheme: URL scheme (optional, for URL rules)
            - hostname: URL hostname (optional, for URL rules)
            - port: URL port (optional, for URL rules)
            - path: URL path (optional, for URL rules)
    """
    settings = Settings.instance()
    rewrite_rules = settings.proxy.rewrite.rewrite_rules(project_id)

    methods = list(kwargs['method'])
    modes = list(kwargs['mode'])
    pattern = kwargs['pattern']

    parameter_rule_dict = _select_parameter_rule(kwargs)
    url_rule_dict = _select_url_rule(kwargs)

    # Filter existing rewrite rules by pattern and methods
    rewrite_rule_filter = lambda rule: rule.pattern == pattern and rule.methods == methods
    filtered_rewrite_rules: List[RewriteRule] = list(filter(rewrite_rule_filter, rewrite_rules))

    if len(filtered_rewrite_rules) == 0:
        # No matching rule found, create a new one
        parameter_rules = list(filter(lambda r: r is not None, [parameter_rule_dict])) if parameter_rule_dict else []
        url_rules = list(filter(lambda r: r is not None, [url_rule_dict])) if url_rule_dict else []

        rewrite_rule = RewriteRule({
            'methods': methods,
            'pattern': pattern,
            'parameter_rules': parameter_rules,
            'url_rules': url_rules,
        })
        rewrite_rules.append(rewrite_rule)
        settings.proxy.rewrite.set_rewrite_rules(project_id, rewrite_rules)
    else:
        # Matching rule(s) found, merge parameter and URL rules
        parameter_rule_filter = lambda rule: parameter_rule_dict and rule.name == parameter_rule_dict.get('name') and rule.type == parameter_rule_dict.get('type') and rule.modes == modes
        url_rule_filter = lambda rule: rule.modes == modes

        for existing_rewrite_rule in filtered_rewrite_rules:
            # Merge parameter rules
            if parameter_rule_dict:
                parameter_rules = existing_rewrite_rule.parameter_rules
                filtered_parameter_rules: List[ParameterRule] = list(filter(parameter_rule_filter, parameter_rules))

                if len(filtered_parameter_rules) == 0:
                    parameter_rule = ParameterRule(parameter_rule_dict)
                    parameter_rules.append(parameter_rule)
                    existing_rewrite_rule.parameter_rules = parameter_rules
                else:
                    for parameter_rule in filtered_parameter_rules:
                        parameter_rule.update(parameter_rule_dict)

            # Merge URL rules
            if url_rule_dict:
                url_rules = existing_rewrite_rule.url_rules
                filtered_url_rules: List[UrlRule] = list(filter(url_rule_filter, url_rules))

                if len(filtered_url_rules) == 0:
                    url_rule = UrlRule(url_rule_dict)
                    url_rules.append(url_rule)
                    existing_rewrite_rule.url_rules = url_rules
                else:
                    for url_rule in filtered_url_rules:
                        url_rule.update(url_rule_dict)

    settings.commit()

