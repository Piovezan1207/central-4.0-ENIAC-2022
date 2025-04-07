# Integração da Alexa com Planta Industrial 4.0 FESTO

Este projeto realiza a integração da assistente virtual **Amazon Alexa** com uma **planta industrial 4.0 da FESTO**, permitindo o controle da planta por meio de comandos de voz. O projeto foi desenvolvido no **Centro Universitário ENIAC**.

## Visão Geral

A arquitetura do sistema é composta por:

- **Skill da Alexa**: Recebe comandos de voz e os converte em requisições HTTP.
- **API Intermediária**: Responsável por receber as requisições da Alexa e retransmiti-las à central local.
- **Central Local**: Interpreta as requisições da API e se comunica diretamente com os **CLPs** e o **controlador do manipulador robótico**.
- **Comunicação Bidirecional**: Permite não só enviar comandos à planta, mas também receber feedbacks do estado atual do sistema.

## Tecnologias Utilizadas

- Amazon Alexa (Skill personalizada)
- API REST (Node.js, Flask, ou similar)
- Controladores Lógicos Programáveis (CLPs)
- Controlador de manipulador robótico FESTO
- Rede local e protocolos industriais

## Funcionalidades

- Controle remoto da planta industrial via comandos de voz.
- Retorno do estado da planta para a Alexa.
- Integração segura e local com os dispositivos industriais.

## Objetivo

Facilitar o controle e a automação da planta 4.0 por meio de tecnologias modernas de voz e IoT, promovendo a conectividade e usabilidade no ambiente industrial.
