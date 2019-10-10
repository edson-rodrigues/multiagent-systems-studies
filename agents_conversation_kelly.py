from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
from pade.behaviours.protocols import TimedBehaviour

# Comportamento do agente Remetente

class RemetenteBehaviour(FipaRequestProtocol):
    
    def __init__(self, agent,message):
        super(RemetenteBehaviour, self).__init__(agent=agent,message=message,is_initiator=True)

    # Este método tem por objetivo exibir a "resposta" da mensagem recebida pelo agente
    def handle_inform(self, message):
        display_message(self.agent.aid.localname, 'O agente {} recebeu a mensagem "{}" da conversa {}'.format(self.agent.aid.localname, message.content, message.conversationID))


# Comportamento do agente Destinatario

class DestinatarioBehaviour(FipaRequestProtocol):

    def __init__(self, agent):
        super(DestinatarioBehaviour, self).__init__(agent=agent,message=None,is_initiator=False)

    # Este método tem por objetivo escrever uma resposta para a mensagem recebida   
    def handle_request(self, message):
        
        super(DestinatarioBehaviour, self).handle_request(message)
        
        # Exibe a mensagem recebida
        display_message(self.agent.aid.localname, 'O agente {} recebeu a mensagem "{}" da conversa {}'.format(self.agent.aid.localname, message.content, message.conversationID))
        
        # Escreve uma resposta para a mensagem recebida
        reply = message.create_reply()
        reply.set_performative(ACLMessage.INFORM)
        reply.set_content('Hello!')
        display_message(self.agent.aid.localname, 'Enviando mensagem...')
        self.agent.send(reply)
        display_message(self.agent.aid.localname, 'Mensagem enviada')


class ComportTemporal(TimedBehaviour):
    
    # Comportamento temporal do remetente
    
    def __init__(self, agent, time, message):
        super(ComportTemporal, self).__init__(agent, time)
        self.message = message

    def on_time(self):
        super(ComportTemporal, self).on_time()
        self.agent.send(self.message)
        display_message(self.agent.aid.localname, 'Mensagem enviada')
        
        
class Remetente(Agent):
    
    def __init__(self, aid):
        # Chamando um construtor da classe 'mãe' = Agente
        super(Remetente, self).__init__(aid=aid, debug=False)
        
        display_message(self.aid.localname, 'Enviando mensagem...')
        
        # Mensagem a ser enviada
        message = ACLMessage(ACLMessage.REQUEST)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(AID(name='destinatario'))
        message.set_content('Ola, eu estou aqui!')
        
        # Adicionando os comportamentos ao agente
        self.behaviours.append(RemetenteBehaviour(self, message))
        # O tempo do comportamento temporal é dado em segundos
        self.behaviours.append(ComportTemporal(self, 5.0, message))


class Destinatario(Agent):

    def __init__(self, aid):
        # Chamando um construtor da classe 'mãe' = Agente
        super(Destinatario, self).__init__(aid=aid, debug=False)
        
        # Adicionando o comportamento do Destinatáro
        self.behaviours.append(DestinatarioBehaviour(self))
        

if __name__ == '__main__':

    agentes = list()
    
    remetente_nome = 'remetente@localhost:9000'
    remetente = Remetente(AID(name=remetente_nome))
    agentes.append(remetente)

    destinatario_nome = 'destinatario@localhost:9001'
    destinatario = Destinatario(AID(name=destinatario_nome))
    agentes.append(destinatario)

    start_loop(agentes)

