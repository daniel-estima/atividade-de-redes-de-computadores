import platform
import subprocess
import socket
import threading

def mostrar_ip():
  print("\n" + "=" * 40 + "\n ENDEREÇO IP\n" + "=" * 40)
  if platform.system() == "Windows":
    subprocess.run('cmd /c ipconfig | findstr /i "IPv4 IP"', shell=True)
  else:
    subprocess.run("ip -brief addr show", shell=True)


def mostrar_gateway():
  print("\n" + "=" * 40 + "\n GATEWAY PADRÃO\n" + "=" * 40)
  if platform.system() == "Windows":
    subprocess.run('cmd /c ipconfig | findstr /i "Gateway"', shell=True)
  else:
    subprocess.run("ip route show | grep default", shell=True)


def mostrar_dns():
  print("\n" + "=" * 40 + "\n SERVIDORES DNS\n" + "=" * 40)
  if platform.system() == "Windows":
    subprocess.run('cmd /c ipconfig /all | findstr /i "DNS"', shell=True)
  else:
    subprocess.run("cat /etc/resolv.conf | grep nameserver", shell=True)


def executar_tracert(destino="google.com"):
  print(f"\n" + "=" * 40 + f"\n EXECUTANDO TRACERT PARA {destino}\n" + "=" * 40)
  comando = (
      ["tracert", destino]
      if platform.system() == "Windows"
      else ["traceroute", destino]
  )
  subprocess.run(comando)


def executar_jitter(destino="google.com"):
  print(f"\n" + "=" * 40 + f"\n EXECUTANDO JITTER PARA {destino}\n" + "=" * 40)
  parametro = "-n" if platform.system() == "Windows" else "-c"
  subprocess.run(["ping", parametro, "10", destino])


def executar_nslookup(destino="google.com"):
  print(f"\n" + "=" * 40 + f"\n EXECUTANDO NSLOOKUP PARA {destino}\n" + "=" * 40)
  subprocess.run(["nslookup", destino])


def receber_mensagens_udp(sock):
  while True:
    try:
      dados, endereco = sock.recvfrom(1024)
      print(f"\n{dados.decode('utf-8')}\n> ", end="")
    except:
      break


def iniciar_chat_udp(nickname):
  porta_local = int(input("Sua porta local para escutar mensagens UDP: "))
  ip_dest = input("IP do destinatário (ou Gateway): ")
  porta_dest = int(input("Porta do destinatário: "))

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind(("0.0.0.0", porta_local))


  t = threading.Thread(target=receber_mensagens_udp, args=(sock,), daemon=True)
  t.start()

  print(f"\n--- CHAT UDP INICIADO ({nickname}) --- (Digite 'sair' para encerrar)")
  while True:
    msg = input("> ")
    if msg.lower() == "sair":
      break
    mensagem_formatada = f"[{nickname} - UDP]: {msg}"
    sock.sendto(mensagem_formatada.encode("utf-8"), (ip_dest, porta_dest))
  sock.close()


def servidor_tcp(porta_local, nickname):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(("0.0.0.0", porta_local))
  sock.listen(1)
  print(f"Aguardando conexão TCP na porta {porta_local}...")
  conn, addr = sock.accept()
  print(f"Conectado com {addr}")

  def receber():
    while True:
      try:
        dados = conn.recv(1024)
        if not dados:
          break
        print(f"\n{dados.decode('utf-8')}\n> ", end="")
      except:
        break

  threading.Thread(target=receber, daemon=True).start()

  while True:
    msg = input("> ")
    if msg.lower() == "sair":
      break
    conn.send(f"[{nickname} - TCP]: {msg}".encode("utf-8"))
  conn.close()
  sock.close()


def cliente_tcp(ip_dest, porta_dest, nickname):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((ip_dest, porta_dest))

  def receber():
    while True:
      try:
        dados = sock.recv(1024)
        if not dados:
          break
        print(f"\n{dados.decode('utf-8')}\n> ", end="")
      except:
        break

  threading.Thread(target=receber, daemon=True).start()

  while True:
    msg = input("> ")
    if msg.lower() == "sair":
      break
    sock.send(f"[{nickname} - TCP]: {msg}".encode("utf-8"))
  sock.close()


def menu_chat():
  nickname = input("Digite seu Nickname: ")
  print("\n--- CHAVE DE SELEÇÃO DE PROTOCOLO ---")
  print("1. UDP")
  print("2. TCP")
  proto = input("Escolha o protocolo (1-2): ")

  if proto == "1":
    iniciar_chat_udp(nickname)
  elif proto == "2":
    modo = input("1. Esperar conexão (Servidor)\n2. Conectar a um IP (Cliente)\nOpção: ")
    if modo == "1":
      porta = int(input("Sua porta local: "))
      servidor_tcp(porta, nickname)
    else:
      ip_dest = input("IP do destinatário: ")
      porta_dest = int(input("Porta do destinatário: "))
      cliente_tcp(ip_dest, porta_dest, nickname)


def menu():
  while True:
    print("\n" + "=" * 30)
    print("      MENU DE REDES")
    print("=" * 30)
    print("1. Mostrar IP")
    print("2. Mostrar GATEWAY")
    print("3. Mostrar DNS")
    print("4. Executar TRACERT")
    print("5. Executar JITTER")
    print("6. Executar nslookup")
    print("7. Abrir CHAT (TCP / UDP)")
    print("8. Sair")

    opcao = input("\nEscolha uma opção (1-8): ")

    if opcao == "1":
      mostrar_ip()
    elif opcao == "2":
      mostrar_gateway()
    elif opcao == "3":
      mostrar_dns()
    elif opcao == "4":
      host = input("Digite o host/IP (Padrão: google.com): ") or "google.com"
      executar_tracert(host)
    elif opcao == "5":
      host = input("Digite o host/IP (Padrão: google.com): ") or "google.com"
      executar_jitter(host)
    elif opcao == "6":
      host = input("Digite o host/IP (Padrão: google.com): ") or "google.com"
      executar_nslookup(host)
    elif opcao == "7":
      menu_chat()
    elif opcao == "8":
      print("Encerrando o programa...")
      break
    else:
      print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
  menu()
