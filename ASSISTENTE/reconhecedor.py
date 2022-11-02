import speech_recognition as sr
from nltk import word_tokenize, corpus
import json
from pygame import mixer 



IDIOMA_CORPUS = "portuguese"
IDIOMA_FALA = "pt-BR"
CAMINHO_CONFIGURACAO = "config.json"

def iniciar():
    global reconhecedor
    global palavras_de_parada
    global nome_assistente
    global acoes
    
    
    reconhecedor= sr.Recognizer()
    palavras_de_parada = set(corpus.stopwords.words(IDIOMA_CORPUS))
    
    with open(CAMINHO_CONFIGURACAO, 'r') as arquivo_configuracao:
        configuracoes = json.load(arquivo_configuracao)
        
        nome_assistente = configuracoes["nome"]
        acoes = configuracoes["acoes"]
        
        arquivo_configuracao.close()

def escutar():
    global reconhecedor
    
    comando = None
    
    with sr.Microphone() as audio:
        reconhecedor.adjust_for_ambient_noise(audio)
        
        print("O que você deseja?")
        fala = reconhecedor.listen(audio, timeout=5, phrase_time_limit=5)
        try:
            comando = reconhecedor.recognize_google(fala, language=IDIOMA_FALA)
        except sr.UnknownValueError:
            print("comando não reconhecido!!!")
    
    return comando
    

def eliminar_palavras(tokens):
    global palavras_de_parada
    
    tokens_filtrados = []
    for token in tokens:
        if token not in palavras_de_parada:
            tokens_filtrados.append(token)
    
    return tokens_filtrados

def tokenizar(comando):
    global nome_assistente
    
    acao = None
    objeto = None
    
    tokens = word_tokenize(comando, IDIOMA_CORPUS)
    if tokens:
        tokens = eliminar_palavras(tokens)
        
        if len(tokens) >= 3:
            if nome_assistente == tokens[0].lower():
                acao = tokens[1].lower()
                objeto = tokens[2].lower()
            
    
    return acao, objeto

def executar_audio():
    mixer.init()
    mixer.music.load("audio.mp3") 

def validar(acao, objeto):
    global acoes
    
    valido = False
    
    if acao and objeto:
        for acaoCadastrada in acoes:
            if acao == acaoCadastrada["nome"]:
                if objeto in acaoCadastrada["objetos"]:
                    valido = True
                
                break
    return valido

def executar(acao, objeto):
    if acao == "ligar":
        if objeto == "som":
             print("O Radio foi ligado!!!")
             executar_audio()
             mixer.music.play() 
        if objeto == "ventilador":
             print("O Ventilador foi ligado!!!")
        if objeto == "ar-condcionado":
             print("O ar-condicionado foi ligado!!!")
        if objeto == "farol":
             print("O farol foi ligado!!!")
    if acao == "desligar":
        if objeto == "som":
            mixer.music.stop() 
            print("O Radio foi desligado!!!")
        if objeto == "ventilador":
             print("O Ventilador foi desligado!!!")
        if objeto == "ar-condcionado":
             print("O ar-condicionado foi  desligado!!!")
        if objeto == "farol":
             print("O farol foi  desligado!!!")
    if acao == "aumentar":
        if objeto == "volume":
            mixer.music.set_volume(0.7)
            print("O volume do som foi aumentado!!!")
        if objeto == "temperatura":
            print("A temperatura do ar-condicionado foi aumentado!!!")     
        if objeto == "velocidade":
            print("O velocidade do ventilador foi aumentada!!!")
    if acao == "diminuir":
        if objeto == "volume":
            mixer.music.set_volume(0.2)
            print("O volume do som foi diminuido!!!")
        if objeto == "temperatura":
            print("A temperatura do ar-condicionado foi diminuida!!!")     
        if objeto == "velocidade":
            print("O velocidade do ventilador foi diminuida!!!") 
            
                 
                
if __name__=="__main__":
    iniciar()
    
    continuar = True
    while continuar:
        try:
            
            comando = escutar()
            
            if comando:
                acao, objeto = tokenizar(comando)
                valido = validar(acao, objeto)
                if valido:
                    executar(acao, objeto)
                else:
                    print("Não entendi , Fale o comando novamente.")
        except KeyboardInterrupt:
            print("Bye!!!")
            
            continuar = False