'''
Ano: 2020
Disciplina: Sistemas de Comunicação
Aluno: Stéfano Campos de Oliveira
Universidade Federal de Santa Catarina

Dependências:
Python 3.8
Tkinter : https://docs.python.org/3/library/tkinter.html
Pyaudio : https://pypi.org/project/PyAudio/
'''


# Includes de bibliotecas
import tkinter as tk
import pyaudio
import wave
import threading as th
from   datetime import datetime

## Definições de funções ##

# Função de início de gravação
# Define e inicia uma thread para a função gravar()
def start():
    global keep_going
    global temp
    keep_going = True
    temp=0
    startButton['state'] = "disabled"
    stopButton['state']  ='normal'
    stopButton.config(bg='#A20101')
    updateTimeStamp()

    # Início de thread para a função gravar()
    thread_record = th.Thread(target=gravar, args=(menuTaxaAmostVar.get(),))
    thread_record.start()

# Função para parar a gravação
# Para o while da thread de gravação e continua o salvamento
def stop():
    global keep_going
    global top
    global temp_id
    keep_going = False
    top.after_cancel(temp_id)
    startButton['state'] = "normal"
    stopButton['state']='disabled'


# Função de gravação do áudio e salvamento de arquivo .wav
# Abre stream de áudio, salva dados em array enquanto botão de 'parar' não for acionado
# constrói arquivo '.wav', fecha e salva arquivo na pasta
def gravar(rate):
    # Declaração de variáveis                                                      
    CHUNK = int(rate/10)
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = rate
    TIMESTAMP = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    WAVE_OUTPUT_FILENAME = "ÁudioPCM " + str(TIMESTAMP) +".wav"

    p = pyaudio.PyAudio() # Instância de PyAudio

    # Parâmetros de stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    
    frames = []

    # Loop de gravação
    while keep_going == True:
        data = stream.read(CHUNK)
        frames.append(data)

    # Encerra e salva o arquivo .wav
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Função para atualizar o tempo de gravação
def updateTimeStamp():
    global temp
    global temp_id
    timestamplabel["text"] = "Duracao: " + "{:.2f}".format(temp/10.0) + " s "
    temp = temp +1
    temp_id = top.after(100, updateTimeStamp)


# Definições de tela de interface
top = tk.Tk()
top.title('Gravador Stefacity')
top.geometry('468x400') 
top.frame()

keep_going= True

# Menu de seleção de Taxa de Amostragem
TaxaAmostList = [8000, 11025, 16000, 22050,32000, 37800,44100, 48000, 88200, 96000, 192000]
menuTaxaAmostVar = tk.IntVar(top)
menuTaxaAmostVar.set(TaxaAmostList[6])
menuTaxaAmost = tk.OptionMenu(top, menuTaxaAmostVar, *TaxaAmostList)
menuTaxaAmost.place(x=205, y=120)
menuTaxaAmost.config(bg='#BDE37C')



# Botões da Interface
# O botão de 'startButton' chama a função 'start()' e botão 'stopButton' chama a função 'stop()'
startButton = tk.Button(top, height=2, width=20, text ="Gravar", command = start, background='#0EB34F', fg='white', activebackground='#04CD53')
startButton.place(x=140, y=200, in_=top)
stopButton = tk.Button(top, height=2, width=20, text ="Encerrar", state=tk.DISABLED,command = stop,background='#5A3434',fg='white' , activebackground='#D90C0C')
stopButton.place(x=140, y=260, in_=top)

# Labels da Interface
titulo_aplicacao = tk.Label(top, text="Gravador de áudio Stefacity", font=("Helvetica", 20))
titulo_aplicacao.place(x=75, y=10)
instrucoes = tk.Label(top, height=3, width=55, background='#F6DFA5', text="Aperte em 'Gravar' para começar uma gravação\nAperte em 'Encerrar' para salvar e encerrar a aplicação\nEscolha a Taxa de Amostragem no menu abaixo")
instrucoes.place(x=10, y=60)
taxa=tk.Label(top, text="Taxa de Amostragem [Hz]:", font=("Helvetica",12))
taxa.place(x=12, y=128)


# Estampa de tempo da Interfacec
temp = 0
temp_id = None
timestamplabel = tk.Label(top, text="Duracao")
timestamplabel.place(x=170, y=350)



# Main Loop Interface
top.mainloop()