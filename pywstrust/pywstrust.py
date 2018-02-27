# -*- coding: utf-8 -*-

"""Main module."""
import requests
from lxml import etree


def build_soap_body(username, password, realm):
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
                https://test-financeweb-se.intrum.com/STS/issue/wstrust/mixed/username
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
            </wst:RequestSecurityToken>
        </s:Body>
    </s:Envelope>
    """.format(username=username, password=password, realm=realm)
    return xml_data


def get_token(username, password, realm):
    soap_body = build_soap_body(
        username,
        password,
        realm
    )
    headers = {'content-type': 'application/soap+xml'}
    response = requests.post(
        'https://test-financeweb-se.intrum.com/STS/issue/wstrust/mixed/username',
        data=soap_body,
        headers=headers
    )

    root = etree.fromstring(response.content)
    token = root.findall(
        ".//saml:Assertion",
        namespaces={'saml': 'urn:oasis:names:tc:SAML:1.0:assertion'}
    )
    return token[0]
