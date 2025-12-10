package lab_4;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class InteractiveClient {
    private static final String SERVER_HOST = "localhost";
    private static final int SERVER_PORT = 12345;

    public static void main(String[] args) {
        try (
                Socket socket = new Socket(SERVER_HOST, SERVER_PORT);
                BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                Scanner scanner = new Scanner(System.in)
        ) {
            System.out.println("Connected to Product Digits Server");
            System.out.println("Enter a number N to find smallest Q with product of digits = N");
            System.out.println("Type 'exit' to quit");
            System.out.println("Example: 24 -> 46 (because 4*6=24)");
            System.out.println("---------------------------------------------------");

            String userInput;
            while (true) {
                System.out.print("\nEnter N: ");
                userInput = scanner.nextLine().trim();

                if (userInput.equalsIgnoreCase("exit")) {
                    out.println("exit");
                    System.out.println("Disconnected from server");
                    break;
                }

                out.println(userInput);
                String response = in.readLine();

                System.out.println("Result: " + response);

                if (response.equals("NO_SOLUTION")) {
                    System.out.println("No natural number Q exists with product of digits = " + userInput);
                }
            }
        } catch (IOException e) {
            System.out.println("Client error: " + e.getMessage());
        }
    }
}
