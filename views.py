from utils import load_data, load_template, append_json, build_response
from urllib.parse import unquote_plus
from database import *
import urllib

db = Database("bancada")


def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for chave_valor in corpo.split('&'):
            if chave_valor[0][0] == 't':
                titulo = unquote_plus(chave_valor)
                params['titulo'] = titulo[7:]
            else:
                detalhe = unquote_plus(chave_valor)
                params['detalhes'] = detalhe[9:]

        # append_json(params)
        note = Note(title=params['titulo'], content=params['detalhes'])
        db.add(note)
        return build_response(code=303, reason='See Other', headers='Location: /')

    # O RESTO DO CÓDIGO DA FUNÇÃO index CONTINUA DAQUI PARA BAIXO...
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(
            title=dados.title, details=dados.content, id=dados.id)
        for dados in db.get_all()
    ]
    notes = '\n'.join(notes_li)

    body = load_template('index.html').format(notes=notes)
    return build_response(body=body)


def delete(id):
    db.delete(id)
    return build_response(code=303, reason='See Other', headers='Location: /')


def note_edit(id):
    note_id = int(id)
    for notes in db.get_all():
        if notes.id == note_id:
            note_object = notes
    body = load_template('edit.html').format(
        title=note_object.title, content=note_object.content, id=note_object.id)
    return build_response(body=body)


def update(id, request):
    id = int(id)

    request = request.replace('\r', '')
    partes = request.split('\n\n')
    corpo = partes[1]
    params = {}
    for chave_valor in corpo.split('&'):
        chave_valor = urllib.parse.unquote_plus(chave_valor)
        if "titulo" in chave_valor:
            params["titulo"] = chave_valor[7:]
        if "detalhes" in chave_valor:
            params["detalhes"] = chave_valor[9:]
    note_object = Note(title=params["titulo"],
                       content=params["detalhes"], id=id)
    db.update(note_object)
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(
            title=note_object.title, details=note_object.content, id=note_object.id, id2=note_object.id)
        for note_object in db.get_all()
    ]
    notes = '\n'.join(notes_li)

    body = load_template('index.html').format(notes=notes)
    return build_response(code=303, reason='See Other', headers='Location: /')


def erro404():
    body = load_template('erro.html')
    return build_response(body=body, code=404)
