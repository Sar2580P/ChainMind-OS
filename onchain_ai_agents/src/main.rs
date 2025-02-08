pub struct Contract {
    pub name: String,
    pub version: String,
}

impl Contract {
    pub fn print_data(&self) {
        println!("{} {}", self.name, self.version);
    }
}

fn main() {
    let contract = Contract {
        name: "onchain_ai_agents".to_string(),
        version: "0.1.0".to_string(),
    };

    contract.print_data();
}
