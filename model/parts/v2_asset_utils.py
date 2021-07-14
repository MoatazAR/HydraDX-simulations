print("running file: asset_utils.py")
import numpy as np

class V2_Asset(): #args
    """
    Asset class is tracking risk assets in a hydra omipool. 
    This includes the shares and weights of those assets.
    Method for adding new asset yet not in existence in the pool
    """  
    def __init__(self, asset_id, reserve, coefficient, price):
        """
        Asset class initialized with 1 risk asset
        """

        self.pool = {
                        # 'asset_id' : asset_id,
                        asset_id :{
                        'R': reserve,
                        'S': reserve,
                        'C': coefficient,
                        'P': price,
                        'dP': 0,   # delta price
                        }}

    def add_new_asset(self, asset_id, reserve, coefficient, price):
        """
        Asset class initialized with 1 risk asset
        """        
        # if price != 'unknown':
        self.pool.update({
                        # 'asset_id' : asset_id,
                        asset_id :{
                        'R': reserve,
                        'S': reserve,
                        'C': coefficient,
                        'P': price}})
        # else calc price

    def add_liquidity_pool(self, asset_id, delta_R, delta_S, delta_C):
        """
        Liquidity added to the pool for one specific risk asset:
        - R increased by delta_R>0
        - S increased by delta_S>0
        - C increased by delta_C>0
        """ 
        # JS July 8, 2021: corrected references to 'pool' attribute
        # Si = self.get_share(asset_id) 
        # Ci = self.get_coefficient(asset_id)
        # Ri = self.get_reserve(asset_id)
        #Y = prev_state['Y']
        #a = params['a']
        for key in self.pool.keys():
            # print(self.pool.items()) 
            if key == asset_id:
                self.pool[key]['R'] += delta_R
                self.pool[key]['S'] += delta_S
                self.pool[key]['C'] += delta_C

    def remove_liquidity_pool(self, asset_id, delta_R, delta_S, delta_C, a):
        """
        Liquidity removed from the pool for one specific risk asset:
        - R decreased by delta_R>0
        - S decreased by delta_S>0
        - C decreased by delta_C>0
        """
        # JS July 8, 2021: corrected references to 'pool' attribute
        Si = self.get_share(asset_id) 
        Ci = self.get_coefficient(asset_id)
        Ri = self.get_reserve(asset_id)
        # Y = prev_state['Y']
        # a = params['a']
        for key in self.pool.keys():
            # print(self.pool.items()) 
            if key == asset_id:
                Si = self.pool[key]['S'] 
                Ci = self.pool[key]['C']
                Ri = self.pool[key]['R']
                self.pool[key]['R'] -= delta_R
                self.pool[key]['S'] -= delta_S
                self.pool[key]['C'] -= delta_C
                self.pool[key]['S'] = Si * (Ri - delta_R) / Ri
                self.pool[key]['C'] = Ci * ((Ri - delta_R) / Ri) ** (a+1)
                #self.pool[key]['W'] += delta_W
                # JS July 8, 2021: 'Y' is a pool constant and is not part of any individual asset
                # The 'Y' pool constant is updated via a mechanism hub
                # self.pool[key]['Y'] = ((Y ** (-a)) - Ci * (Ri ** (-a)) + Ci_plus * ((Ri - delta_R) ** (-a))) ** (- (1 / a))


    def q_to_r_pool(self, asset_id, delta_R):
        """
        In a 'q to r' swap the update of the pool variable for the traded asset:
        - R decreased by delta_R
        """ 
        for key in self.pool.keys():
            # print(self.pool.items()) 
            if key == asset_id:
                self.pool[key]['R'] -= delta_R

    def r_to_q_pool(self, asset_id, delta_R):
        """
        In a 'r to q' swap the update of the pool variable for the traded asset:
        - R increased by delta_R
        """
        for key in self.pool.keys():
            # print(self.pool.items()) 
            if key == asset_id:
                self.pool[key]['R'] += delta_R

    def get_price(self, asset_id):
        """
        returns price P of one specific asset from the pool variable
        """
        for key in self.pool.keys():
            # print(self.pool.items()) 
            if key == asset_id:
                return(self.pool[key]['P'])

    def get_reserve(self, asset_id):
        """
        returns reserve R of one specific asset from the pool variable
        """
        for key in self.pool.keys():
            # print(self.pool.items()) 
            if key == asset_id:
                return(self.pool[key]['R'])

    def get_share(self, asset_id):
        """
        returns share S of one specific asset from the pool variable
        """
        for key in self.pool.keys():
            # print(self.pool.items()) 
            if key == asset_id:
                return(self.pool[key]['S'])

    def get_weight(self, asset_id):
        """
        returns weight W of one specific asset from the pool variable
        """
        for key in self.pool.keys():
            # print(self.pool.items()) 
            if key == asset_id:
                return(self.pool[key]['W'])

    def get_coefficient(self, asset_id):
        """
        returns coefficient C of one specific asset from the pool variable
        """
        for key in self.pool.keys():
            # print(self.pool.items()) 
            if key == asset_id:
                return(self.pool[key]['C'])

    # JS July 8, 2021: this method is not used in the V2 Spec
    ##########
    # def update_price(self, Q, Wq):
    #    """
    #    updates price P of one specific asset from the pool variable and change in price dP for a Q and Sq according to
    #    P = (Q/Sq)/(R/S)
    #    dP = P - P
    #    """        
    #    for key in self.pool.keys():
    #        R = self.pool[key]['R']
    #        S = self.pool[key]['S']
    #        P = self.pool[key]['P']
    #        W = self.pool[key]['W']
    #
    #        self.pool[key]['P'] = (Q/Wq)/(R/W)
    #        self.pool[key]['dP'] = self.pool[key]['P'] - P
    ##########

    # JS July 8, 2021: this method is not used in the V2 Spec
    ##########
    # def update_price_q_i(self, Ki, Q, Sq):
    #    """
    #    updates price according to mechanism specification from 3-3-21
    #    """  
    #    for key in self.pool.keys():
    #        R = self.pool[key]['R']
    #        S = self.pool[key]['S']
    #        P = self.pool[key]['P']

        ###############################################################################################
        ########### YELLOW BOX HYDRA SPEC SWAP RISK ASSETS 3-3-21 #####################################
        #    first_term = Ki / R
        #    second_term_fraction = (Q / Sq) / (R / S)
        #    price_q_i = first_term - second_term_fraction * np.log(R)
        ########### YELLOW BOX HYDRA SPEC SWAP RISK ASSETS 3-3-21 #####################################
        ###############################################################################################

    #       self.pool[key]['P'] = price_q_i
    ##########

    # JS July 8, 2021: method updated according to V2 Spec
    def update_price_a(self, Q, Y, a):
        """
        updates prices for all risk assets according to V2 Spec
        adds an attribute 'dP = P - P_new'
        """  
        for key in self.pool.keys():
            R = self.pool[key]['R']
            P = self.pool[key]['P']
            C = self.pool[key]['C']

            self.pool[key]['P'] = (Q * Y**(a)) * (C / R**(a+1))
            self.pool[key]['dP'] = self.pool[key]['P'] - P

            # print('POOL Class ', ' A value = ', a, ' Spot Price ',spot_price,'Class Price = ', self.pool['i']['P'])
            # print('POOL Class ', ' A value = ', a, 'Asset ', key, ' Class Price = ', self.pool['i']['P'])
        
        # print('POOL Class ', ' A value = ', a, ' R over W= ', R/W,'Q over Wq = ', Q/Wq)

    # JS July 8, 2021: this methiod is not used in the V2 Spec
    ########## 
    # def update_weight(self):
    #    """
    #    updates weight of specific asset from the pool variable according to
    #    W = S
    #    """ 
    #    for key in self.pool.keys():
    #        S = self.pool[key]['S']
    #        self.pool[key]['W'] = S
    ##########

    ## Balance Asset Share Swap
    def swap_share_pool(self, asset_id, delta_S):
        """
        updates share of specific asset from the pool variable for a swap according to
        S = S + delta_S
        """ 
        for key in self.pool.keys():
            # print(self.pool.items()) 
            if key == asset_id:
                self.pool[key]['S'] += delta_S
    
    def swap_weight_pool(self, asset_id, delta_W):
        """
        updates weight of specific asset from the pool variable for a swap according to
        W = W + delta_W
        """ 
        for key in self.pool.keys():
            # print(self.pool.items()) 
            if key == asset_id:
                self.pool[key]['W'] += delta_W

    def __str__(self):
        """
        Print all attributes of an event
        """
        return str(self.__class__) + ": " + str(self.__dict__)     
print("end of file: asset_utils.py")