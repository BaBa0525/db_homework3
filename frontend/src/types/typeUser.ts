type User = {
    account?: String,
    phone?: String,
    password?: String,
    realname?: String,
    role?: 'user' | 'owner',
    shopname?: String,
    latitude?: number,
    longitude?: number,
    balance?: number
};