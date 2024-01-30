import g4f
import asyncio
import threading
import time

from g4f.models import default
    
class GPT:
    def __init__(self, model = g4f.models.default, prePrompt= None, debug = False, logging = None) -> None:
        self.model = model
    

        self.logging = logging
        self._debug = debug

        self._providers = [
    g4f.Provider.GeekGpt,
    g4f.Provider.FakeGpt,
    g4f.Provider.OnlineGpt,
    g4f.Provider.AiChatOnline,
    g4f.Provider.ChatBase,
    g4f.Provider.AiAsk,
    g4f.Provider.Aichat,        
    g4f.Provider.AItianhu,      
    g4f.Provider.AItianhuSpace, 
    g4f.Provider.base_provider, 
    g4f.Provider.Berlin,        
    g4f.Provider.Bing,
    g4f.Provider.ChatAnywhere,      
    g4f.Provider.ChatForAi,     
    g4f.Provider.Chatgpt4Online,
    g4f.Provider.ChatgptAi,     
    g4f.Provider.ChatgptDemo,   
    g4f.Provider.ChatgptDemoAi,
    g4f.Provider.ChatgptFree,
    g4f.Provider.ChatgptLogin,
    g4f.Provider.ChatgptNext,
    g4f.Provider.ChatgptX,
    g4f.Provider.DeepInfra,
    g4f.Provider.FreeGpt,
    g4f.Provider.GPTalk,
    g4f.Provider.GptChatly,
    g4f.Provider.GptForLove,
    g4f.Provider.GptGo,
    g4f.Provider.GptGod,
    g4f.Provider.GptTalkRu,
    g4f.Provider.Hashnode,
    g4f.Provider.Koala,
    g4f.Provider.Liaobots,
    g4f.Provider.Llama2,
    g4f.Provider.MyShell,
    g4f.Provider.Opchatgpts,
    g4f.Provider.PerplexityAi,
    g4f.Provider.Phind,
    g4f.Provider.Pi,
    g4f.Provider.retry_provider,
    g4f.Provider.TalkAi,
    g4f.Provider.Vercel,
    g4f.Provider.Ylokh,
    g4f.Provider.You,
    g4f.Provider.Yqcloud
]

        self.history = []

        if prePrompt:
            self._system_message(prePrompt)

        if self.logging:
            self._load_log()

        self.requestIsDone = False

    def _system_message(self, message: str) -> None:
        self.history.append({'role': 'system', 'content': message})
        self.log_history() if self.logging else None

    def _load_log(self):
        try:
            print(f'load from {self.logging}') if self._debug else None
            with open(self.logging, 'r', encoding='utf-8') as log_file:
                self.history = eval(log_file.read())

        except:
            print(f'file {self.logging} not found. History will be empty.') if self._debug else None

    def log_history(self):
        with open(self.logging, 'w', encoding='utf-8') as log_file:
            log_file.write(f'{self.history}\n')

    def clear_log(self):
        with open(self.logging, 'w', encoding='utf-8') as log_file:
            log_file.write('[]')

    def add_to_chat_history(self, request: list) -> None:
        self.history.append(request)

    def switch_chhat_history(self, request: list) -> None:
        self.history = request

    async def _send_async_request(self, provider) -> None:
        try:
            result = await g4f.ChatCompletion.create_async(
                    model=self.model,
                    messages=self.history,
                    provider=provider
                )
            
            if len(result) >= 5:
                print(provider.__name__) if self._debug else None
                self.requestIsDone = True
                self.history.append({'role': 'assistant', 'content': result})
            
        except:
            print('Error in provider', provider.__name__) if self._debug else None
        

    def send_message(self, request: dict) -> str:
        import time

        startTime = time.time()
        self.history.append(request)

        for provider in self._providers:
            
            asyncio.run(self._send_async_request(provider))
            if self.requestIsDone:
                
                self.requestIsDone = False
                break

        completion = self.history[-1]['content']

        endTime = time.time()
        print(round(endTime - startTime, 2), 'секунд') if self._debug else None
        self.log_history() if self.logging else None


        return completion
    

class GPT_asynco(GPT):
    def __init__(self, model=g4f.models.default, prePrompt=None, debug=False, logging=None) -> None:
        super().__init__(model, prePrompt, debug, logging)

    async def send_message(self, request: dict) -> str:
        import time

        startTime = time.time()
        self.history.append(request)

        for provider in self._providers:
            
            await self._send_async_request(provider)
            if self.requestIsDone:
                
                self.requestIsDone = False
                break

        completion = self.history[-1]['content']

        endTime = time.time()
        print(round(endTime - startTime, 2), 'секунд') if self._debug else None
        self.log_history() if self.logging else None

        return completion




def main():
#     DND_prePrompt = """
# Ты - ИИ помощник мастера подземелий в настоьной ролевой игре. Тебе будет приходить задание и вопросы по НРИ, а ты будешь проявлять креативность и помогать пользователю.
# """
    # gpta = GPT(prePrompt='Ты - ИИ ассистент по имени Анви. Я - Ваня (Иван). У тебя есть доступ к истории чата. Ты способен ее читать и делать на ее основе выводы. Так же ты можешь передавать эту историю пользователь при необходимости.', debug=True)
    gpta = GPT()

#     print(gpta.send_message({'role': 'user', 'content': """
# Привет! Я делаю партию для настольной ролевой игры в сеттинге темного фентези. Суть в чем:
# Персонажи - наемники, которые по причинам (придумай 5 из них) работают на мафию большого города.
# Текущая задача - в письме (напиши его содержимое и от кого оно) рассказывается, что это их последняя задание, после которого они будут свободны.
# Задача - собрать долг с небольшой деревушке в паре километров от города. Их задача собрать ровно 3500 серебрянных монет, дрогоценные камни весом в 5 кг, а так же голова главы деревни.
# Если персонажи не выполнят поручение, то будут казнены.
# """
# }))
    while True: 
        print(gpta.send_message({'role': 'user', 'content': input('>>> ')}))


if __name__ == '__main__':
    main()