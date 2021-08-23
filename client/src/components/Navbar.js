import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'

import { Navbar, Nav, Container } from 'react-bootstrap'
import { FaRegUserCircle, FaHome, FaEye, FaWeight } from 'react-icons/fa'

const NavbarComp = () => {
  return (
    <Navbar collapseOnSelect expand="md" bg="dark" variant="dark">
      <Container>
        <Navbar.Brand style={{ color: 'teal' }}>EoS Monitor</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/home">
              <FaHome style={{ marginRight: 5, marginLeft: 5, marginBottom: 5}} />
              Home</Nav.Link>
            <Nav.Link href="/concept">
              <FaEye style={{ marginRight: 5, marginLeft: 5, marginBottom: 5}}/>
              Concept
            </Nav.Link>
          </Nav>
          <Nav>
            
            <Nav.Link href="/profile" eventKey="disabled" disabled>
              <FaRegUserCircle style={{ marginRight: 5, marginLeft: 5, marginBottom: 5 }} />
              Account
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>           
  )
}

export default NavbarComp