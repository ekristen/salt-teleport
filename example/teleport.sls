teleport-config:
  file.managed:
    - name: /etc/teleport.yaml
    - template: jinja
    - source: salt://config.tmpl
    - defaults:
        token: {{ salt['teleport.node_authentication_token']('role:teleport-auth', expr_form='grain') }}

teleport-service:
  service.running:
    - name: teleport
    - enable: True
    - reload: True
    - watch:
      - file: teleport-config
