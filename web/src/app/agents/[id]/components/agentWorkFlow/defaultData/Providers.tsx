import { v4 } from "uuid";
const Providers = [
  {
    id: v4(),
    about: "Blockchain for fee payments",
    metadata: {
      description:
        "Using blockchain for immutable and transparent fee payments.",
    },
    type: "new-agent",
    name: "New Agent",
  },
];

export default Providers;
