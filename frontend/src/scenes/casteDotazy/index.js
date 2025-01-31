import React from "react";
import {
    Box,
    Accordion,
    AccordionSummary,
    AccordionDetails,
    Typography,
    Divider,
    Container,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import Navbar from "../navbar";

// Func to generate Accordion
const createAccordionSection = (title, content) => (
    <Accordion key={title} className="helper-accordion">
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography fontWeight={"bold"} fontSize={"1rem"}>
                {title}
            </Typography>
        </AccordionSummary>
        <Divider />
        <AccordionDetails>
            <Typography variant="h6" fontSize={"0.9rem"}>
                {content}
            </Typography>
        </AccordionDetails>
    </Accordion>
);

const CasteDotazy = () => {
    return (
        <Box paddingBottom="3rem">
            <Navbar />
            <Typography
                variant="h2"
                align="center"
                sx={{
                    marginTop: "3rem",
                    fontWeight: 700,
                    fontStyle: "italic",
                }}
            >
                FAQ
            </Typography>
            <Container sx={{ maxWidth: "md", mt: 5 }}>
                {createAccordionSection(
                    "Jak ShareTaxMax funguje?",
                    "Po nahrání CSV souborů v části konverter máte na výběr, zda chcete data spojit pro vlastní kontrolu, nebo chcete výpočet v PDF formátu. ShareTaxMax používá metodu FIFO a bere v potaz hodnotový i časový test."
                )}
                {createAccordionSection(
                    "Brutto vs Netto",
                    "Co dělat v případě, že hranice Brutto přesáhla 100 000 korun, ale Netto je pod touto hranicí ? Na tento případ je potřeba si dát pozor, zda-li nastane a je třeba brát v potaz, že daň se vypočítává z rozdílu mezi prodejní a nákupní cenou. Pokud tedy částka Brutto přesáhne 100 000kč, máte povinnost podat daňové přiznání."
                )}
                {createAccordionSection(
                    "Jaké jsou daňové povinnosti spojené s prodejem akcií?",
                    "Jednoduše řečeno, pokud příjmy (NE ZISK) překročí limit 100 000 Kč, máte povinnost podat daňové přiznání a danit částku přesahující 100 000 Kč."
                )}

                {createAccordionSection(
                    "Jaké jsou daňové sazby pro zisky z prodeje akcií?",
                    "V rámci fyzických osob se jedná o sazbu 15%, a v případě, že jste za zdaňovací období prodali 48násobek průměrné mzdy za daný rok, tak daníte 23% sazbou. V roce 2022 tato částka byla 1 867 728 Kč."
                )}

                {createAccordionSection(
                    "Co je to hodnotový test?",
                    "Tento test se zaměřuje především na menší investory. Uvádí, že od zdanění jsou osvobozeni lidé, jejichž příjmy z prodeje cenných papírů nepřesáhly v daném zdaňovacím období 100 000 Kč."
                )}

                {createAccordionSection(
                    "Co je to časový test?",
                    "Časový test na rozdíl od hodnotového platí i pro zámožnější investory. Tento test nám říká, že pokud byla doba mezi nákupem a prodejem cenného papíru delší než 3 roky, je daná osoba zcela osvobozena od daně."
                )}
                {createAccordionSection(
                    "Jaký kurz měn se používá?",
                    "ShareTaxMax počítá v EUR."
                )}
            </Container>
            <Typography
                variant="h2"
                align="center"
                sx={{
                    marginTop: "4rem",
                    fontWeight: 700,
                    fontStyle: "italic",
                }}
            >
                Co ShareTaxMax neumí
            </Typography>
            <Container sx={{ maxWidth: "md", mt: 5 }}>
                {createAccordionSection(
                    "Neumí počítat dividendy z akcií",
                    "Danění dividend je mimo rozsah této aplikace a tedy nedokáže problém vyřešit. Pro každou zemi je individuální daňová sazba a tedy záleží kde se společnost, která nám vyplací dividendy nachází. Taktéž zaleží zda má Česká Republika s danou zemí podepsaný formulář o dvojím zdanění. "
                )}

                {createAccordionSection(
                    "Omezení na měnu",
                    "Většina investorů obchoduje v EUR, protože se jedná o nejvýhodnější variantu a tedy v tuto chvíli je to omezeno pouze na EUR"
                )}
            </Container>
        </Box>
    );
};

export default CasteDotazy;
