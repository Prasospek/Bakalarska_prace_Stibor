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
                variant="h4" // Change the variant to h2 for a bigger font size
                align="center" // Keep the alignment centered
                sx={{
                    marginTop: "4rem", // Increase the marginTop value for more spacing
                    fontWeight: 700, // Add font weight for emphasis
                    fontStyle: "italic", // Add italic style
                }}
            >
                FAQ
            </Typography>
            <Container maxWidth="md" sx={{ mt: 5 }}>
                <Accordion
                    sx={{
                        marginBottom: 2,
                        "&.Mui-expanded": {
                            border: "1px solid #000", // Add border style when expanded
                        },
                    }}
                >
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                    >
                        <Typography fontWeight={"bold"}>
                            Jak se daní ?
                        </Typography>
                    </AccordionSummary>
                    <Divider />
                    <AccordionDetails>
                        <Typography>
                            Lorem ipsum dolor sit amet, consectetur adipisicing
                            elit. Quasi tempore blanditiis explicabo numquam,
                            quisquam sit nemo unde tempora dolor, nesciunt
                            itaque modi optio ad molestiae, impedit magnam
                            perspiciatis dolore cumque!
                        </Typography>
                    </AccordionDetails>
                </Accordion>
                <Accordion
                    sx={{
                        marginBottom: 2,
                        "&.Mui-expanded": {
                            border: "1px solid #000", // Add border style when expanded
                        },
                    }}
                >
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="panel1a-header"
                    >
                        <Typography fontWeight={"bold"}>
                            Jak na daně s dividendy ?
                        </Typography>
                    </AccordionSummary>
                    <Divider />
                    <AccordionDetails>
                        <Typography>
                            Lorem ipsum dolor sit amet consectetur adipisicing
                            elit. Dignissimos porro odio consectetur eum! Labore
                            sunt libero voluptates harum dignissimos quis?
                            Inventore voluptatum iure reiciendis officia
                            consequuntur reprehenderit quos excepturi, quia
                            minus amet dolorum tempore, nulla porro neque,
                            corporis itaque ratione aliquid sint dignissimos
                            minima? Qui quas maxime excepturi nisi neque.
                        </Typography>
                    </AccordionDetails>
                </Accordion>
            </Container>
        </div>
    );
};

export default CasteDotazy;
