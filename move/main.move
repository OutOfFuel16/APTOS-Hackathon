module MyModule::P2PCurRental {

    use aptos_framework::signer;
    use std::vector;

    struct Crypto has store, key {
        owner: address,
        model: vector<u8>,
        is_available: bool,
    }

    public fun list_cur(owner: &signer, model: vector<u8>) {
        let cur = Crypto {
            owner: signer::address_of(owner),
            model,
            is_available: true,
        };
        move_to(owner, cur);
    }

    public fun rent_cur(renter: &signer, owner_address: address) acquires Crypto {
        let cur = borrow_global_mut<Cur>(owner_address);

        assert!(cur.is_available, 1);

        cur.is_available = false;
    }
}