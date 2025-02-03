const _DUMMY_USER: UserType = {
  name: "Shivam",
  email: "",
  role: "admin",
};

interface UserType {
  name: string;
  email: string;
  role: string;
}

export { type UserType, _DUMMY_USER };
