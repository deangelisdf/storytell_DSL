script SanMartino

actor Giacomo
actor Lucia

dialogue {
    Lucia: "Hey you!"
    Giacomo: "Me?"
    Lucia: "Yeah! Where we are?"
    Giacomo: if a == +1 { 
        a = 0; 
    } elif a == 2 {
        a = 1;
        b = 2;
        if c < 1 
        {
            c = 2;
        }
    }
    else { b = 1; }
}