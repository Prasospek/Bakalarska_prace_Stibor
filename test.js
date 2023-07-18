{
    /* Step 6 */
}
<Box display="flex" alignItems="center" marginTop={5} paddingBottom={5}>
    <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        width={40}
        height={40}
        borderRadius="50%"
        bgcolor="blue"
        color="white"
        fontSize={20}
        fontWeight={700}
    >
        6
    </Box>
    <Box ml={2}>
        <Typography variant="h4" fontWeight={700}>
            Krok 6: Nahrejte data do konverteru
        </Typography>
        <Typography variant="h5">
            V případě že prodávate akcie musíte zadat csv soubor i v období kdy
            jste danou akcii pořídili. Bohužel CSV od Trading212 neobsahuje
            informaci, kdy byla daná akcie pořízena a tedy nelze zjistit, zda je
            aplikovatelný <i>Časový test</i> (Více podrobností v FQA){" "}
            <b>!!!PŘIDAT SEM LINK !!!</b> . <br></br> <b>Příklad: </b> v roce
            2021 jste prodali akcie Apple za 150 000Kč. V případě, že podáte
            výpis pouze z roku 2021 software vyhodnotí, že nemáte nárok na úlevu
            od daně skrz časový test a platí normální danění. Pokud ovšem
            prokážete dle výpisu z roku např 2017, že jste pořídil akcie Apple
            za 120 000kč bude Vám uleveno od daně.
        </Typography>
    </Box>
</Box>
