use functions::plus_one;

mod functions;

fn main() {
    println!("Hello, world!");

    functions::another_function(5);
    functions::print_labeled_masurement(45, '$');

    let x = functions::five();

    println!("The value of x is: {x}");

    let x = plus_one(x);

    println!("The value of x (shadowed) is: {x}");
}
