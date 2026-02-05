import re

class Validator:
    valid_san: re.Pattern[str] = re.compile(r"""
                                    (
                                        (O-O)\+?

                                      | (O-O-O)\+?

                                      | (0-0)\+?

                                      | (0-0-0)\+?

                                      | ([a-h]
                                            (x[a-h][1-8])
                                          | [1-8]
                                        [NBRQK]?\+?)

                                      | ([NBRQK]
                                        ([a-h][1-8])?
                                        x?[a-h][1-8]\+/)

                                      | (R[a-h]|[1-8]x?[a-h][1-8]\+?)
                                    )
                                    """, re.VERBOSE)