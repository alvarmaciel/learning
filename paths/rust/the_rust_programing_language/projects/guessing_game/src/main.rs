use rand::random_range;
use std::cmp::Ordering;
use std::io;

fn main() {
    println!("Guess the number!");

    let secret_number = random_range(1..=100);

    loop {
        println!("Please input your guess!");

        let mut guess = String::new(); // new es una función asociada que crea una instancia de String en este caso unida a la variable

        io::stdin()
            .read_line(&mut guess) // el & incdica que este argumento es una referencia. da una forma de acceder  a una parte desde multiples lados
            .expect("Failed to read line");

        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        println!("You guessed: {guess}");

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too Big"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }
}
