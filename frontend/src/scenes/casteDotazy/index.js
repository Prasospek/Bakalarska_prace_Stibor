import React, { useEffect } from "react";
import {
    Accordion,
    AccordionSummary,
    AccordionDetails,
    Typography,
    Divider,
    Container,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import Navbar from "../navbar";

// Custom function to generate an accordion section
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
        <div>
            <Navbar />
            <Typography
                variant="h2"
                align="center"
                sx={{
                    marginTop: "4rem",
                    fontWeight: 700,
                    fontStyle: "italic",
                }}
            >
                FAQ
            </Typography>
            <Container sx={{ maxWidth: "md", mt: 5 }}>
                {/* Accordion Section 1 */}
                {createAccordionSection(
                    "Jaké jsou daňové povinnosti spojené s prodejem akcií?",
                    "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quasi tempore blanditiis explicabo numquam, quisquam sit nemo unde tempora dolor, nesciunt itaque modi optio ad molestiae, impedit magnam perspiciatis dolore cumque!"
                )}

                {/* Accordion Section 2 */}
                {createAccordionSection(
                    "Jaké jsou daňové povinnosti spojené s vyplácením dividend z akcií?",
                    "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quasi tempore blanditiis explicabo numquam, quisquam sit nemo unde tempora dolor, nesciunt itaque modi optio ad molestiae, impedit magnam perspiciatis dolore cumque!"
                )}

                {/* Accordion Section 3 */}
                {createAccordionSection(
                    "Jaké jsou daňové sazby pro zisky z prodeje akcií?",
                    "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quasi tempore blanditiis explicabo numquam, quisquam sit nemo unde tempora dolor, nesciunt itaque modi optio ad molestiae, impedit magnam perspiciatis dolore cumque!"
                )}

                {/* Accordion Section 4 */}
                {createAccordionSection(
                    "Co je to hodnotový test ?",
                    "Tento test se zaměřuje především na menší investory. Uvádí, že od zdanění jsou osvobozeni lidé, jejichž příjmy z prodeje cenných papíru nepřesáhlo v daném zdaňovacím období 100 000 Kč."
                )}

                {/* Accordion Section 5 */}
                {createAccordionSection(
                    "Co je to časový test ?",
                    "Časový test narozdíl od hodnotového platí i pro zámožnější investory. Tento test nám říká, že pokud od doby mezi nákupem a prodejem cenného papíru byla delší doba než 3 roky, tak je daná osoba zcela osvobozena od daně."
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
                {/* Accordion Section 6 */}
                {createAccordionSection(
                    "Jaké jsou daňové povinnosti spojené s prodejem akcií?",
                    "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quasi tempore blanditiis explicabo numquam, quisquam sit nemo unde tempora dolor, nesciunt itaque modi optio ad molestiae, impedit magnam perspiciatis dolore cumque!"
                )}

                {/* Accordion Section 7 */}
                {createAccordionSection(
                    "Jaké jsou daňové povinnosti spojené s vyplácením dividend z akcií?",
                    "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quasi tempore blanditiis explicabo numquam, quisquam sit nemo unde tempora dolor, nesciunt itaque modi optio ad molestiae, impedit magnam perspiciatis dolore cumque!"
                )}

                {/* Accordion Section 8 */}
                {createAccordionSection(
                    "Jaké jsou daňové sazby pro zisky z prodeje akcií?",
                    "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quasi tempore blanditiis explicabo numquam, quisquam sit nemo unde tempora dolor, nesciunt itaque modi optio ad molestiae, impedit magnam perspiciatis dolore cumque!"
                )}

                {/* Accordion Section 9 */}
                {createAccordionSection(
                    "Co je to hodnotový test ?",
                    "Tento test se zaměřuje především na menší investory. Uvádí, že od zdanění jsou osvobozeni lidé, jejichž příjmy z prodeje cenných papíru nepřesáhlo v daném zdaňovacím období 100 000 Kč."
                )}

                {/* Accordion Section 10 */}
                {createAccordionSection(
                    "Co je to časový test ?",
                    "Časový test narozdíl od hodnotového platí i pro zámožnější investory. Tento test nám říká, že pokud od doby mezi nákupem a prodejem cenného papíru byla delší doba než 3 roky, tak je daná osoba zcela osvobozena od daně."
                )}
            </Container>
        </div>
    );
};

export default CasteDotazy;
