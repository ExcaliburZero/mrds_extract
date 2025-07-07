struct Monster {
    u8 name[12];
    u8 unknown_a[28];
    u16 power;
    u16 intelligence;
    u16 skill;
    u16 speed;
    u16 defense;
    u16 life;
    u8 unknown_b[368];
};

struct SaveEntry {
    u8 unknown_a[10];
    u8 ranch_name[13];
    u8 unknown_b[4];
    u8 player_name[13];
    u8 unknown_c[416];
    Monster monsters[31];
    u8 unknown_d[2108];
};

struct SaveFile {
    u8 header[34];
    SaveEntry entries[2];
};

SaveFile save @ 0x0;