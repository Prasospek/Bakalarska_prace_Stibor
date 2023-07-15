import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { Container, Divider } from "@mui/material";
import Navbar from "../navbar";

const CasteDotazy = () => {
    return (
        <div>
            <Navbar />
            <Typography
                variant="h2" // Change the variant to h2 for a bigger font size
                align="center" // Keep the alignment centered
                sx={{
                    marginTop: "4rem", // Increase the marginTop value for more spacing
                    fontWeight: 700, // Add font weight for emphasis
                    fontStyle: "italic", // Add italic style
                }}
            >
                FAQ
            </Typography>
            <Container sx={{ maxWidth: "md", mt: 5 }}>
                <Accordion className="helper-accordion">
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                    >
                        <Typography fontWeight={"bold"} fontSize={"1rem"}>
                            Jaké jsou daňové povinnosti spojené s prodejem
                            akcií?
                        </Typography>
                    </AccordionSummary>
                    <Divider />
                    <AccordionDetails>
                        <Typography variant="h6" fontSize={"0.9rem"}>
                            Lorem ipsum dolor sit amet, consectetur adipisicing
                            elit. Quasi tempore blanditiis explicabo numquam,
                            quisquam sit nemo unde tempora dolor, nesciunt
                            itaque modi optio ad molestiae, impedit magnam
                            perspiciatis dolore cumque!
                        </Typography>
                    </AccordionDetails>
                </Accordion>
                <Accordion className="helper-accordion">
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                    >
                        <Typography fontWeight={"bold"} fontSize={"1rem"}>
                            Jaké jsou daňové povinnosti spojené s vyplácením
                            dividend z akcií?
                        </Typography>
                    </AccordionSummary>
                    <Divider />
                    <AccordionDetails>
                        <Typography variant="h6" fontSize={"0.9rem"}>
                            Lorem ipsum dolor sit amet, consectetur adipisicing
                            elit. Quasi tempore blanditiis explicabo numquam,
                            quisquam sit nemo unde tempora dolor, nesciunt
                            itaque modi optio ad molestiae, impedit magnam
                            perspiciatis dolore cumque!
                        </Typography>
                    </AccordionDetails>
                </Accordion>
                <Accordion className="helper-accordion">
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                    >
                        <Typography fontWeight={"bold"} fontSize={"1rem"}>
                            Jaké jsou daňové sazby pro zisky z prodeje akcií?
                        </Typography>
                    </AccordionSummary>
                    <Divider />
                    <AccordionDetails>
                        <Typography variant="h6" fontSize={"0.9rem"}>
                            Lorem ipsum dolor sit amet, consectetur adipisicing
                            elit. Quasi tempore blanditiis explicabo numquam,
                            quisquam sit nemo unde tempora dolor, nesciunt
                            itaque modi optio ad molestiae, impedit magnam
                            perspiciatis dolore cumque!
                        </Typography>
                    </AccordionDetails>
                </Accordion>
                <Accordion className="helper-accordion">
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                    >
                        <Typography fontWeight={"bold"} fontSize={"1rem"}>
                            Co je to hodnotový test ?
                        </Typography>
                    </AccordionSummary>
                    <Divider />
                    <AccordionDetails>
                        <Typography variant="h6" fontSize={"0.9rem"}>
                            Tento test se zaměřuje především na menší investory.
                            Uvádí, že od zdanění jsou osvobozeni lidé, jejichž
                            příjmy z prodeje cenných papíru nepřesáhlo v daném
                            zdaňovacím období <b>100 000 Kč.</b>
                        </Typography>
                    </AccordionDetails>
                </Accordion>
                <Accordion className="helper-accordion">
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                    >
                        <Typography fontWeight={"bold"} fontSize={"1rem"}>
                            Co je to časový test ?
                        </Typography>
                    </AccordionSummary>
                    <Divider />
                    <AccordionDetails>
                        <Typography variant="h6" fontSize={"0.9rem"}>
                            Časový test narozdíl od hodnotového platí i pro
                            zámožnější investory. Tento test nám říká, že pokud
                            od doby mezi nákupem a prodejem cenného papíru byla
                            delší doba než <b>3 roky</b> tak je daná osoba zcela
                            osvobozena od daně..
                        </Typography>
                    </AccordionDetails>
                </Accordion>
            </Container>
        </div>
    );
};

export default CasteDotazy;
