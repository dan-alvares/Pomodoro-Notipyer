from notifypy import Notify
from PySimpleGUI import PySimpleGUI as sg


# 1 ciclo pomodoro = 25 min = 1500 segundos
# OK exibir tempo restante do ciclo na tela
# OK exibir quantidade de ciclos
# OK ao finalizar ciclo, tocar som de alerta COM notificação

# Após 1 ciclo, realizar pausa de 5 min = 300 segundos
# - ao finalizar pausa, tocar som de alerta - > escolher som de alerta para pausa
# - criar função timer para pausa

# Após 4 ciclos concluídos, realizar pausa longa de 15 a 30 min = 900 / 1800 segundos
# - exibir alerta de notificação
# - perguntar se deseja iniciar novo ciclo ou finalizar

# OK Reiniciar ciclo para seguir tarefas


def notificacao(meu_titulo='Título Teste', texto_notificacao='Texto Teste'):
    notifica = Notify()
    notifica.title = meu_titulo
    notifica.message = texto_notificacao
    notifica.audio = 'files/sound/alerta.wav'
    return notifica.send()


titulo = 'Pomodoro Notipyer '
fim_tarefa = 'Tarefa concluída!'


def formatar_tempo(t):
    mins, secs = divmod(t, 60)
    tempo_formatado = '{:02d}:{:02d}'.format(mins, secs)
    return tempo_formatado


ciclos_realizados = 0

sg.theme('Reddit')

layout = [[sg.Text('Ciclos:'), sg.Text('0', key='CICLOS')],
          [sg.Text('00:00', size=(8, 2), font=('Helvetica', 20),
                   justification='center', key='TIMER')],
          [sg.Text('-HOLDER TXT-')],
          [sg.Button('Iniciar', key='INICIAR', focus=True, button_color=('black', 'white')),
           sg.Button('Pausar', key='PAUSAR', focus=False, disabled=True, button_color=('black', 'white')),
           sg.Button('Resetar', key='RESETAR', focus=False, disabled=True, button_color=('black', 'white'))]]

app = sg.Window('Notipyer Pomodoro', layout, auto_size_buttons=False, keep_on_top=False,
                grab_anywhere=True,
                element_padding=(0, 0),
                finalize=True,
                element_justification='c')

contador_esta_ativo, tempo_restante = False, 5  # contador inicia desativado // tempo do timer pomodoro em segundos

# Loop de Eventos do App
while True:
    evento, valores = app.Read(1000)
    tempo_restante -= 1 * (contador_esta_ativo is True)

    if evento == 'INICIAR':
        contador_esta_ativo = True
        if tempo_restante == 0:
            tempo_restante = 10
        app['INICIAR'].Update(disabled=True)
        app['PAUSAR'].Update(disabled=False)
        app['RESETAR'].Update(disabled=False)

    elif evento == 'PAUSAR':
        contador_esta_ativo = False
        app['INICIAR'].Update('Continuar', disabled=False)
        app['PAUSAR'].Update(disabled=True)

    elif evento == 'RESETAR':
        tempo_restante = 10
        contador_esta_ativo = False
        app['INICIAR'].Update('Iniciar', disabled=False)
        app['PAUSAR'].Update(disabled=True)
        app['RESETAR'].Update(disabled=True)

    elif tempo_restante == 0 and contador_esta_ativo:  # fim da contagem
        notificacao(titulo, fim_tarefa)
        tempo_restante = 0
        ciclos_realizados += 1
        app['CICLOS'].Update(f'{ciclos_realizados}')
        contador_esta_ativo = False

        if evento == 'INICIAR':
            tempo_restante = 10
            app['INICIAR'].Update(disabled=True)
            app['PAUSAR'].Update(disabled=False)
            app['RESETAR'].Update(disabled=False)
        app['INICIAR'].Update('Reiniciar', disabled=False)
        app['PAUSAR'].Update(disabled=True)
        app['RESETAR'].Update(disabled=True)

    elif evento is None or evento == 'Quit':
        break

    app['TIMER'].Update(formatar_tempo(tempo_restante))
