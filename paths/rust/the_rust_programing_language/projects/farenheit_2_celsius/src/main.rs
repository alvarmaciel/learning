use clap::Parser;

//// Convert a Farenheit Temperature to Celsius
#[derive(Parser)]
struct Cli {
    temperature: f32,
    scale: char,
}

fn main() {
    // A cli that asks for a temp in far and converts to cel
    let args = Cli::parse();
    // Get the temperature value to a variable
    let temperature: f32 = args.temperature;
    let scale: String = args.scale.to_uppercase().to_string();

    if scale == "F" {
        // Convert to celsius
        let temperature_in_celsius: f32 = (temperature - 32.0) * 5.0 / 9.0;
        println!(
            "{temperature} {scale} represents {:?} in Celsius",
            temperature_in_celsius
        );
    } else if scale == "C" {
        let temperature_in_farenheits: f32 = (temperature * 1.8) + 32.0;
        println!(
            "{temperature} {scale} represents {:?} in Farenheits",
            temperature_in_farenheits
        );
    } else {
        println!("Please use c or f to define the scale of the temperature to convert");
    }
}
