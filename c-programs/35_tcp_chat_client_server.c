/*
 * Program  : 35_tcp_chat_client_server.c
 * Title    : Simple TCP Chat Application (Client-Server)
 * Author   : Lydia S. Makiwa
 * Date     : 2026-06-01
 *
 * Description:
 *   A simple TCP-based chat program demonstrating socket programming,
 *   client-server architecture, and concurrent connections.
 *   The server can handle multiple clients using fork().
 *   This is foundational for understanding how networked applications
 *   like WhatsApp, Discord, and Zoom work at the protocol level.
 *
 * Compilation:
 *   Server: gcc -o server 35_tcp_chat_client_server.c -DSERVER_MODE
 *   Client: gcc -o client 35_tcp_chat_client_server.c
 *
 * Run:
 *   ./server  (listens on port 8080)
 *   ./client  (connects to localhost:8080)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <signal.h>
#include <time.h>

#define PORT 8080
#define BUFFER_SIZE 1024
#define MAX_CLIENTS 10
#define SERVER_IP "127.0.0.1"

/* ANSI colour codes for nicer output */
#define RESET "\033[0m"
#define GREEN "\033[32m"
#define CYAN  "\033[36m"
#define YELLOW "\033[33m"
#define RED   "\033[31m"

void print_timestamp() {
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    char buffer[20];
    strftime(buffer, sizeof(buffer), "%H:%M:%S", t);
    printf("[%s] ", buffer);
}

/* ---------- SERVER FUNCTIONS ---------- */
#ifdef SERVER_MODE

void handle_client(int client_sock, struct sockaddr_in client_addr) {
    char buffer[BUFFER_SIZE];
    char client_ip[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &(client_addr.sin_addr), client_ip, INET_ADDRSTRLEN);
    int client_port = ntohs(client_addr.sin_port);
    
    printf(GREEN "[SERVER] New connection from %s:%d\n" RESET, 
           client_ip, client_port);
    
    /* Send welcome message */
    char *welcome = 
        "\n" CYAN "=== Welcome to Lydia's Chat Server! ===\n" RESET
        "Type your message and press Enter.\n"
        "Type 'quit' to disconnect.\n\n";
    send(client_sock, welcome, strlen(welcome), 0);
    
    /* Chat loop */
    while (1) {
        memset(buffer, 0, BUFFER_SIZE);
        int bytes_received = recv(client_sock, buffer, BUFFER_SIZE - 1, 0);
        
        if (bytes_received <= 0) {
            printf(YELLOW "[SERVER] Client %s:%d disconnected\n" RESET,
                   client_ip, client_port);
            break;
        }
        
        buffer[bytes_received] = '\0';
        
        /* Remove trailing newline */
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len - 1] == '\n') {
            buffer[len - 1] = '\0';
        }
        
        print_timestamp();
        printf(CYAN "[%s:%d] %s\n" RESET, client_ip, client_port, buffer);
        
        if (strcmp(buffer, "quit") == 0 || strcmp(buffer, "exit") == 0) {
            char *bye = "Goodbye!\n";
            send(client_sock, bye, strlen(bye), 0);
            break;
        }
        
        /* Echo back with server acknowledgment */
        char response[BUFFER_SIZE];
        snprintf(response, BUFFER_SIZE, 
                 "[Server ACK] Received: '%s' (%zu chars)",
                 buffer, strlen(buffer));
        send(client_sock, response, strlen(response), 0);
    }
    
    close(client_sock);
    exit(0);
}

int run_server() {
    int server_sock, client_sock;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len = sizeof(client_addr);
    
    /* Create socket */
    server_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (server_sock < 0) {
        perror(RED "[ERROR] Socket creation failed" RESET);
        exit(1);
    }
    
    /* Allow reuse of address */
    int opt = 1;
    if (setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
        perror(RED "[ERROR] setsockopt failed" RESET);
        exit(1);
    }
    
    /* Configure server address */
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);
    
    /* Bind */
    if (bind(server_sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror(RED "[ERROR] Bind failed" RESET);
        exit(1);
    }
    
    /* Listen */
    if (listen(server_sock, MAX_CLIENTS) < 0) {
        perror(RED "[ERROR] Listen failed" RESET);
        exit(1);
    }
    
    printf(GREEN "\n=========================================\n");
    printf("  Lydia's TCP Chat Server — Running\n");
    printf("  Listening on port %d\n", PORT);
    printf("  Max clients: %d\n", MAX_CLIENTS);
    printf("=========================================\n" RESET);
    printf("\nWaiting for connections...\n\n");
    
    /* Handle SIGCHLD to prevent zombie processes */
    signal(SIGCHLD, SIG_IGN);
    
    /* Accept connections in a loop */
    while (1) {
        client_sock = accept(server_sock, 
                            (struct sockaddr*)&client_addr, &addr_len);
        if (client_sock < 0) {
            perror(RED "[ERROR] Accept failed" RESET);
            continue;
        }
        
        /* Fork a child process to handle this client */
        pid_t pid = fork();
        if (pid == 0) {
            /* Child process */
            close(server_sock);
            handle_client(client_sock, client_addr);
        } else if (pid > 0) {
            /* Parent process */
            close(client_sock);
            printf(GREEN "[SERVER] Spawned child PID %d for new client\n" RESET, pid);
        } else {
            perror(RED "[ERROR] Fork failed" RESET);
        }
    }
    
    close(server_sock);
    return 0;
}

#endif /* SERVER_MODE */


/* ---------- CLIENT FUNCTIONS ---------- */
#ifndef SERVER_MODE

int run_client() {
    int client_sock;
    struct sockaddr_in server_addr;
    char buffer[BUFFER_SIZE];
    char username[50] = "Anonymous";
    
    /* Create socket */
    client_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (client_sock < 0) {
        perror(RED "[ERROR] Socket creation failed" RESET);
        exit(1);
    }
    
    /* Configure server address */
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    
    if (inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr) <= 0) {
        perror(RED "[ERROR] Invalid address / Address not supported" RESET);
        exit(1);
    }
    
    printf(YELLOW "Enter your username: " RESET);
    if (fgets(username, sizeof(username), stdin)) {
        size_t len = strlen(username);
        if (len > 0 && username[len - 1] == '\n') {
            username[len - 1] = '\0';
        }
    }
    
    /* Connect to server */
    if (connect(client_sock, (struct sockaddr*)&server_addr, 
                sizeof(server_addr)) < 0) {
        perror(RED "[ERROR] Connection failed" RESET);
        printf("   Is the server running? Try: ./server\n");
        exit(1);
    }
    
    printf(GREEN "\n✅ Connected to chat server at %s:%d\n" RESET, 
           SERVER_IP, PORT);
    
    /* Receive welcome message */
    memset(buffer, 0, BUFFER_SIZE);
    recv(client_sock, buffer, BUFFER_SIZE - 1, 0);
    printf("%s", buffer);
    
    printf(YELLOW "💬 Chatting as [%s] — type 'quit' to exit\n\n" RESET, username);
    
    /* Chat loop */
    while (1) {
        /* Construct message with username */
        printf(YELLOW "You > " RESET);
        
        if (fgets(buffer, BUFFER_SIZE, stdin) == NULL) {
            break;
        }
        
        /* Remove trailing newline */
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len - 1] == '\n') {
            buffer[len - 1] = '\0';
        }
        
        /* Format message with username */
        char msg[BUFFER_SIZE + 60];
        snprintf(msg, sizeof(msg), "[%s] %s", username, buffer);
        
        send(client_sock, msg, strlen(msg), 0);
        
        if (strcmp(buffer, "quit") == 0 || strcmp(buffer, "exit") == 0) {
            break;
        }
        
        /* Receive server response */
        memset(buffer, 0, BUFFER_SIZE);
        int bytes = recv(client_sock, buffer, BUFFER_SIZE - 1, 0);
        if (bytes <= 0) {
            printf(RED "\n⚠ Connection closed by server\n" RESET);
            break;
        }
        buffer[bytes] = '\0';
        
        printf(CYAN "Server > %s\n\n" RESET, buffer);
    }
    
    close(client_sock);
    printf(YELLOW "\n👋 Disconnected. Thanks for chatting!\n" RESET);
    return 0;
}

#endif /* !SERVER_MODE */


/* ===== MAIN ===== */
int main() {
    printf("=");
    for (int i = 0; i < 52; i++) printf("=");
    printf("\n");
    printf("   TCP CHAT APPLICATION — CLIENT-SERVER\n");
    printf("   Socket Programming Demo\n");
    for (int i = 0; i < 52; i++) printf("=");
    printf("\n\n");
    
#ifdef SERVER_MODE
    printf(CYAN "Starting in SERVER mode...\n" RESET);
    return run_server();
#else
    printf(CYAN "Starting in CLIENT mode...\n" RESET);
    printf("  Compile with -DSERVER_MODE to build the server.\n\n");
    return run_client();
#endif
}
