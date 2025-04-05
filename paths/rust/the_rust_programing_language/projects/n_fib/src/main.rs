struct Cli {
    number: u64,
}

fn fibo(numero: u64) -> u64 {
    // Base cases for standard Fibonacci: F(0)=0, F(1)=1
    if numero <= 1 {
        numero // Implicit return for 0 or 1
    } else {
        // Recursive step: F(n) = F(n-1) + F(n-2)
        // The result of this expression is implicitly returned
        fibo(numero - 1) + fibo(numero - 2)
    }
}
fn main() {
    let arg = std::env::args().nth(1).expect("Number expected");

    let number: u64 = match arg.trim().parse() {
        Ok(num) => num,
        Err(_) => {
            // Handle the error case properly
            eprintln!("Error: '{}' is not a valid non-negative integer.", arg);
            std::process::exit(1); // Exit if parsing fails
        }
    };

    let cli_args = Cli { number }; // Renamed variable to avoid shadowing 'arg' unnecessarily

    // Call fibo and potentially print the result (optional, but good practice)
    let result = fibo(cli_args.number);
    println!("Fibonacci({}) = {}", cli_args.number, result);
}
