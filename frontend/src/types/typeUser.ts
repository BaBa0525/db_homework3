export type User = {
  account?: string;
  phone?: string;
  password?: string;
  realname?: string;
  role?: "user" | "owner";
  shopname?: string;
  latitude?: number;
  longitude?: number;
  balance?: number;
};
