import SatelliteObservation

test = SatelliteObservation.Satellite(256, 145, 0.00012, 56, 50)
data = SatelliteObservation.AffichageSatellites(1000,
                                                SatelliteObservation.Satellite.calcul_parametres_ellipse(test)[0],
                                                SatelliteObservation.Satellite.calcul_parametres_ellipse(test)[1],
                                                SatelliteObservation.Satellite.calcul_parametres_ellipse(test)[2],
                                                SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(test)[
                                                    0],
                                                SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(test)[
                                                    1],
                                                SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(test)[
                                                    2],
                                                256, 145, 56, 50)

data.get_data()
data.animate()
