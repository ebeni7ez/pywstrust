# -*- coding: utf-8 -*-

"""Main module."""
import requests
from lxml import etree


def build_soap_body(username, password, base_url, realm, client_id=None):
    on_behalf_of = ""
    if client_id:
        on_behalf_of = """
        <auth:AdditionalContext xmlns:auth="http://docs.oasis-open.org/wsfed/authorization/200706">
            <auth:ContextItem Name="urn:asn/claims/identity/onBehalfOfClientId">
                <auth:Value>{client_id}</auth:Value>
            </auth:ContextItem>
        </auth:AdditionalContext>
        """.format(client_id=client_id)

    xml_data = """
    <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope">
        <s:Header>
            <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                <wsse:UsernameToken
                        xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"
                        wsu:Id="Me">
                    <wsse:Username>{username}</wsse:Username>
                    <wsse:Password>{password}</wsse:Password>
                </wsse:UsernameToken>
            </wsse:Security>
            <wsa:To xmlns:wsa="http://www.w3.org/2005/08/addressing">
                {base_url}STS/issue/wstrust/mixed/username
            </wsa:To>
            <wsa:Action xmlns:wsa="http://www.w3.org/2005/08/addressing">
                http://docs.oasis-open.org/ws-sx/ws-trust/200512/RST/Issue
            </wsa:Action>
        </s:Header>
        <s:Body>
            <wst:RequestSecurityToken xmlns:wst="http://docs.oasis-open.org/ws-sx/ws-trust/200512">
                <wst:TokenType>http://docs.oasis-open.org/wss/oasis-wss-saml-token-profile-1.1#SAMLV1.1</wst:TokenType>
                <wst:RequestType>http://docs.oasis-open.org/ws-sx/ws-trust/200512/Issue</wst:RequestType>
                <wsp:AppliesTo xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy">
                    <wsa:EndpointReference xmlns:wsa="http://www.w3.org/2005/08/addressing">
                        <wsa:Address>{realm}</wsa:Address>
                    </wsa:EndpointReference>
                </wsp:AppliesTo>
                <wst:KeyType>http://docs.oasis-open.org/ws-sx/ws-trust/200512/Bearer</wst:KeyType>
                {on_behalf_of}
            </wst:RequestSecurityToken>
        </s:Body>
    </s:Envelope>
    """.format(
        username=username,
        password=password,
        realm=realm,
        on_behalf_of=on_behalf_of,
        base_url=base_url
    )
    return xml_data


def get_token(username, password, base_url, realm, client_id=None):
    soap_body = build_soap_body(
        username,
        password,
        base_url,
        realm,
        client_id
    )
    headers = {'content-type': 'application/soap+xml'}
    response = requests.post(
        '{base_url}STS/issue/wstrust/mixed/username'.format(base_url=base_url),
        data=soap_body,
        headers=headers
    )

    root = etree.fromstring(response.content)
    token = root.findall(
        ".//saml:Assertion",
        namespaces={'saml': 'urn:oasis:names:tc:SAML:1.0:assertion'}
    )
    if token:
        return token[0]
    return None
