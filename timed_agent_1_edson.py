from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
from pade.behaviours.protocols import TimedBehaviour

class SenderComportamento(FipaRequestProtocol):
    
    def __init__(self, agent,message):
        super(SenderComportamento, self).__init__(agent=agent,message=message,is_initiator=True)

    def handle_request(self, message):
        display_message(self.agent.aid.localname, 'O agente {} recebeu a mensagem "{}" da conversa {}'.format(self.agent.aid.localname, message.content, message.conversationID))


class ListenerComportamento(FipaRequestProtocol):

    def __init__(self, agent):
        super(ListenerComportamento, self).__init__(agent=agent,message=None,is_initiator=False)

    
    def handle_request(self, message):
        
        super(ListenerComportamento, self).handle_request(message)
        
        
        display_message(self.agent.aid.localname, 'O agente {} recebeu a mensagem "{}" da conversa {}'.format(self.agent.aid.localname, message.content, message.conversationID))
        
        reply = message.create_reply()
        reply.set_performative(ACLMessage.INFORM)
        reply.set_content('Oi, o que deseja?')
        display_message(self.agent.aid.localname, 'Enviando mensagem...')
        self.agent.send(reply)
        display_message(self.agent.aid.localname, 'Mensagem enviada')


class ComportTemporal(TimedBehaviour):
            
    def __init__(self, agent, time, message):
        super(ComportTemporal, self).__init__(agent, time)
        self.message = message

    def on_time(self):
        super(ComportTemporal, self).on_time()
        self.agent.send(self.message)
        display_message(self.agent.aid.localname, 'Mensagem enviada')
        
        
class Sender(Agent):
    
    def __init__(self, aid):
        super(Sender, self).__init__(aid=aid, debug=False)
        
        display_message(self.aid.localname, 'Enviando mensagem...')
        
        message = ACLMessage(ACLMessage.REQUEST)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(AID(name='ouvinte'))
        message.set_content('Ola, eu estou aqui!')
        
        self.behaviours.append(SenderComportamento(self, message))
        
        self.behaviours.append(ComportTemporal(self, 5.0, message))


class Listener(Agent):

    def __init__(self, aid):
        
        super(Listener, self).__init__(aid=aid, debug=False)
        
        
        self.behaviours.append(ListenerComportamento(self))
        

if __name__ == '__main__':

    agentes = list()
    
    sender_nome = 'sender@localhost:9000'
    sender = Sender(AID(name=sender_nome))
    agentes.append(sender)

    listener_nome = 'destinatario@localhost:9001'
    listener = Listener(AID(name=listener_nome))
    agentes.append(listener)

    start_loop(agentes)

