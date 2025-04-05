use std::io;

fn main() {
    let a = [1, 2, 3, 4, 5];

    println!("Please enter an array index.");

    let mut index = String::new();

    io::stdin()
        .read_line(&mut index)
        .expect("Failes to read line");

    let index: usize = index.trim().parse().expect("index entered is not a number");

    let element = a[index];

    println!("The valie of the element at index {index} is {element}");
}
